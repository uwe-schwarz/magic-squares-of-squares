from __future__ import annotations
import unittest
from classes import CLASSES
from prime_power_rigidity import gaussian_normalized_offsets,half_slope_unit,initial_branches,lift_once,normalized_offsets
from targeted_reconstruction import exact_offsets,verify_candidate
class PrimePowerTests(unittest.TestCase):
 def test_exact_class_fixture(self):self.assertEqual(len(CLASSES),16);self.assertEqual(len({c[0] for c in CLASSES}),16)
 def test_half_slope_is_norm_one(self):
  for bits in range(4,13):
   m=1<<bits
   for x in range(min(32,1<<(bits-2))):
    a,b=half_slope_unit(x,m);self.assertEqual((a*a+b*b)%m,1)
 def test_torus_matches_direct_gaussian_ratio(self):
  js=CLASSES[0][2]
  for bits in (6,8,10):
   m=1<<bits
   for xs in ((0,1,2),(1,3,5),(2,5,7)):
    generators=tuple((1,2*x) for x in xs);self.assertEqual(normalized_offsets(js,xs,m),gaussian_normalized_offsets(js,generators,m))
 def test_factor_two_is_observable(self):
  js=CLASSES[0][2];m=256;correct=normalized_offsets(js,(1,2,3),m)
  from prime_power_rigidity import cmul,cpow
  units=[half_slope_unit(x,m) for x in (1,2,3)];wrong=[]
  for col in range(4):
   z=(1,0)
   for row in range(3):z=cmul(z,cpow(units[row],int(js[row][col]),m),m)
   wrong.append(z[1]%m)
  self.assertNotEqual(correct,tuple(wrong))
 def test_counter_for_counter_lift(self):
  js=CLASSES[0][2];b4=initial_branches(js,4);b5=lift_once(js,b4,5);direct=initial_branches(js,5);key=lambda b:(b.xs,b.signs,b.edge_swap);self.assertEqual({key(x) for x in b5},{key(x) for x in direct})
 def test_exact_reembedding_rejects_toy_triple(self):
  js=CLASSES[0][2];generators=((2,1),(3,2),(4,1));self.assertEqual(len(exact_offsets(js,generators)),4);self.assertFalse(verify_candidate(js,generators).coupled)
if __name__=='__main__':unittest.main()
