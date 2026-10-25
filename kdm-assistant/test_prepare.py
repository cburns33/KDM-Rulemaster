"""Verify asset rebuilding after the source relocation."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import prepare


class PrepareTests(unittest.TestCase):
    def test_rebuild_uses_sources_directory(self):
        page_map = Path(__file__).resolve().parents[1] / 'sources' / 'KDM_Rules_Focused_Page_Map.md'
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'project'
            app = project / 'kdm-assistant'
            (app / 'data').mkdir(parents=True)
            (project / 'sources').mkdir()
            shutil.copyfile(page_map, project / 'sources' / page_map.name)
            pdf = project / 'sources' / 'KDM_Rulebook_1.5_Rules_Focused.pdf'
            pdf.touch()

            def render(command, check):
                self.assertTrue(check)
                self.assertEqual(command[-2], str(pdf))
                for page in range(1, 139):
                    (app / 'public' / 'pages' / f'render-{page:03}.jpg').touch()

            with patch.object(prepare, 'ROOT', app), patch.object(prepare.subprocess, 'run', side_effect=render) as renderer:
                prepare.prepare()
            renderer.assert_called_once()
            manifest = json.loads((app / 'data' / 'manifest.json').read_text(encoding='utf-8'))
            self.assertEqual(len(manifest), 138)
            self.assertEqual(manifest[0]['original'], 2)
            self.assertEqual(manifest[89]['printed'], 125)
            self.assertTrue((app / 'public' / 'pages' / '138.jpg').is_file())
            self.assertTrue((app / 'data' / 'source-manifest.json').is_file())


if __name__ == '__main__':
    unittest.main()
