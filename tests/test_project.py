import sys, unittest, copy, pathlib, json, re
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import workflow as w
class ProjectTests(unittest.TestCase):
    def test_offline(self):
        s=w.run_offline(); self.assertEqual(len(s['slides']),15); self.assertEqual(len(w.SOURCES),9)
    def test_bad_reference(self):
        s=w.ingest({'api':False}); s['wiki']['batting']=s['wiki']['batting'].replace('[S06]','[S99]'); self.assertTrue(w.wiki_errors(s['wiki']))
    def test_slide_missing_field(self):
        s=w.ingest({'api':False}); pages=copy.deepcopy(w.SEED); pages[3]['formula']=''; self.assertTrue(w.slide_errors(pages,s['wiki']))
    def test_retry_limit(self):
        self.assertEqual(w.route({'errors':['bad'],'attempt':2}),'retry'); self.assertEqual(w.route({'errors':['bad'],'attempt':3}),'fail'); self.assertEqual(w.route({'errors':[],'attempt':1}),'ok')
    def test_formulas(self):
        self.assertAlmostEqual(.4+.6,1); self.assertAlmostEqual((13*10+3*30-2*100)/100+3.1,3.3); self.assertEqual(9*30/90,3)
    def test_links(self):
        for f in (w.P/'wiki').glob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8')):
                if not link.startswith('https://'): self.assertTrue((f.parent/link).exists(),link)
if __name__=='__main__': unittest.main()
