"""Behavioral regressions for truthful inventory claims and output preservation."""
from pathlib import Path
import importlib.util
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[2]/'convert/build_inventory.py'
spec=importlib.util.spec_from_file_location('inventory',SCRIPT)
inventory=importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
    def scan(self,rows):
        return inventory.build_inventory({'datasets':rows},{'classes':['can','paper']},self.root)
    def ds(self,name='one',enabled=True):return {'name':name,'local_root':name,'enabled':enabled}
    def test_missing_root_is_unknown_not_empty(self):
        r=self.scan([self.ds()]);self.assertIsNone(r['datasets'][0]['images'])
        self.assertEqual(r['datasets'][0]['scan_state'],'missing_root')
        self.assertEqual(r['totals']['missing_roots'],1)
    def test_existing_empty_root_is_distinct(self):
        (self.root/'one').mkdir();r=self.scan([self.ds()])
        self.assertEqual(r['datasets'][0]['images'],0)
        self.assertEqual(r['datasets'][0]['scan_state'],'scanned')
    def test_disabled_root_with_files_is_not_counted(self):
        (self.root/'one').mkdir();(self.root/'one'/'a.jpg').touch()
        r=self.scan([self.ds(enabled=False)])
        self.assertIsNone(r['datasets'][0]['images']);self.assertEqual(r['totals']['images'],0)
        self.assertEqual(r['totals']['disabled_roots'],1)
    def test_recursive_suffix_count_without_claiming_valid_media(self):
        root=self.root/'one'/'nested';root.mkdir(parents=True)
        for name in ('a.JPG','b.png','annotations.json','note.txt'):(root/name).touch()
        r=self.scan([self.ds()]);self.assertEqual(r['datasets'][0]['images'],2)
        self.assertIn('filename',r['evidence_type'])
    def test_configured_classes_are_not_observed_and_annotations_unknown(self):
        (self.root/'one').mkdir();r=self.scan([self.ds()])
        self.assertEqual(r['configured_classes'],['can','paper'])
        self.assertIsNone(r['datasets'][0]['classes_seen'])
        self.assertIsNone(r['datasets'][0]['annotations']);self.assertIsNone(r['totals']['annotations'])
    def test_existing_output_preserved_until_explicit_overwrite(self):
        p=self.root/'inventory.json';p.write_text('original',encoding='utf-8')
        with self.assertRaises(FileExistsError):inventory.write_inventory(p,{'schema_version':2})
        self.assertEqual(p.read_text(),'original')
        inventory.write_inventory(p,{'schema_version':2},True)
        self.assertIn('schema_version',p.read_text())
    def test_invalid_enabled_string_is_not_truthy(self):
        with self.assertRaises(ValueError):self.scan([self.ds(enabled='false')])
    def test_non_directory_root_is_not_silently_empty(self):
        (self.root/'one').touch()
        with self.assertRaises(ValueError):self.scan([self.ds()])

if __name__=='__main__':unittest.main()
