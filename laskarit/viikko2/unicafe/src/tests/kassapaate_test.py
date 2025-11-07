import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_kassapaatteen_saldo_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_myytyjen_lounaiden_maara_on_nolla(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_edullisen_lounaan_osto_kateisella(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(250)

        self.assertEqual(vaihtoraha, 10)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.40)
    
    def test_edullisen_lounaan_osto_kateisella_kun_maksu_ei_ole_riittava(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(100)

        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_maukkaan_lounaan_osto_kateisella(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.00)

    def test_maukkaan_lounaan_osto_kateisella_kun_maksu_ei_ole_riittava(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(10)

        self.assertEqual(vaihtoraha, 10)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_edullisen_lounaan_osto_kortilla(self):
        onnistui = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)

        self.assertEqual(onnistui, True)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_edullisen_lounaan_osto_kortilla_kun_maksu_ei_ole_riittava(self):
        kortti = Maksukortti(100)

        onnistui = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(onnistui, False)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_maukkaan_lounaan_osto_kortilla(self):
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertEqual(onnistui, True)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_maukkaan_lounaan_osto_kortilla_kun_maksu_ei_ole_riittava(self):
        kortti = Maksukortti(100)
        
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(onnistui, False)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_rahan_lataaminen_kortille_onnistuu(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 1000)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1010.00)
    
    def test_negatiivisen_rahamaaran_lataaminen_kortille_epäonnistuu(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1234)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
