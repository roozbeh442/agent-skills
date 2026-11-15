from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import install


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="agent skills tests ")
        self.root = Path(self.temporary.name) / "repository with spaces"
        self.home = Path(self.temporary.name) / "home with spaces"
        self.skill = self.root / "skills" / "sample-skill"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: Test skill.\n---\n\nInstructions.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def destinations(self) -> list[Path]:
        return [root / "sample-skill" for root in install.destination_roots(self.home)]

    def test_symlink_install_works_from_unrelated_working_directory(self) -> None:
        original = Path.cwd()
        unrelated = Path(self.temporary.name) / "unrelated"
        unrelated.mkdir()
        try:
            os.chdir(unrelated)
            results = install.run_install(self.root, self.home)
        finally:
            os.chdir(original)
        self.assertTrue(all(result.status == "changed" for result in results))
        for destination in self.destinations():
            self.assertTrue(destination.is_symlink())
            self.assertEqual(destination.resolve(), self.skill.resolve())

    def test_repeated_symlink_install_is_noop(self) -> None:
        install.run_install(self.root, self.home)
        results = install.run_install(self.root, self.home)
        self.assertTrue(all(result.status == "ok" for result in results))

    def test_real_directory_is_never_overwritten(self) -> None:
        destination = self.destinations()[0]
        destination.mkdir(parents=True)
        (destination / "keep.txt").write_text("keep", encoding="utf-8")
        results = install.run_install(self.root, self.home)
        result = next(item for item in results if item.destination == destination)
        self.assertEqual(result.status, "conflict")
        self.assertEqual((destination / "keep.txt").read_text(encoding="utf-8"), "keep")

    def test_incorrect_symlink_requires_explicit_replacement(self) -> None:
        destination = self.destinations()[0]
        destination.parent.mkdir(parents=True)
        wrong = self.root / "wrong"
        wrong.mkdir()
        destination.symlink_to(wrong, target_is_directory=True)
        first = install.install_one(
            self.skill,
            destination,
            mode="symlink",
            check=False,
            dry_run=False,
            replace_links=False,
        )
        self.assertEqual(first.status, "conflict")
        replaced = install.install_one(
            self.skill,
            destination,
            mode="symlink",
            check=False,
            dry_run=False,
            replace_links=True,
        )
        self.assertEqual(replaced.status, "changed")
        self.assertEqual(destination.resolve(), self.skill.resolve())

    def test_check_and_dry_run_do_not_write(self) -> None:
        checked = install.run_install(self.root, self.home, check=True)
        self.assertTrue(all(result.status == "missing" for result in checked))
        preview = install.run_install(self.root, self.home, dry_run=True)
        self.assertTrue(all(result.status == "changed" for result in preview))
        self.assertTrue(all(not destination.exists() for destination in self.destinations()))

    def test_managed_copy_updates_but_unmanaged_copy_does_not(self) -> None:
        install.run_install(self.root, self.home, mode="copy")
        for destination in self.destinations():
            self.assertTrue((destination / install.COPY_MARKER).is_file())

        (self.skill / "SKILL.md").write_text("updated\n", encoding="utf-8")
        check = install.run_install(self.root, self.home, mode="copy", check=True)
        self.assertTrue(all(result.status == "outdated" for result in check))
        updated = install.run_install(self.root, self.home, mode="copy")
        self.assertTrue(all(result.status == "changed" for result in updated))
        for destination in self.destinations():
            self.assertEqual(
                (destination / "SKILL.md").read_text(encoding="utf-8"), "updated\n"
            )

        unmanaged = self.destinations()[0]
        (unmanaged / install.COPY_MARKER).unlink()
        result = install.install_one(
            self.skill,
            unmanaged,
            mode="copy",
            check=False,
            dry_run=False,
            replace_links=False,
        )
        self.assertEqual(result.status, "conflict")


if __name__ == "__main__":
    unittest.main()
