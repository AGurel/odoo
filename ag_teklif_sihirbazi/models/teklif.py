from math import ceil

from odoo import api, fields, models


class Teklif(models.Model):
    _name = "teklif"
    _inherit = ['mail.thread']
    _description = "Teklif Sihirbazı teklif kayıtları"

    baslik = fields.Char(string="Teklif Başlığı", required=True, tracking=True)
    teklif_tarihi = fields.Datetime(string="Teklif Tarihi", required=True, tracking=True)
    gecerlilik_tarihi = fields.Datetime(string="Geçerlilik Tarihi", required=True, tracking=True)
    musteri_id = fields.Many2one("res.partner", "Müşteri", required=True, tracking=True)
    kumes_tipi = fields.Selection([("Broyler", "Broyler"), ("Damızlık", "Damızlık")], string="Kümes Tipi", default="Broyler", required=True, tracking=True)
    yapi = fields.Selection([("Betonarme", "Betonarme"), ("Konstrüksiyon", "Konstrüksiyon")], default="Betonarme", string="Yapı", required=True, tracking=True)
    ortadan_bolme = fields.Selection([("Evet", "Evet"), ("Hayır", "Hayır")], default="Evet", string="Ortadan Bölme", required=True, tracking=True)
    kumes_uzunluk = fields.Integer(string="Kümes Uzunluk (m)", required=True, tracking=True)
    kumes_genislik = fields.Integer(string="Kümes Genişlik (m)", required=True, tracking=True)
    yan_duvar_yuksekligi = fields.Integer(string="Yan Duvar Yük. (m)", required=True, tracking=True)
    mahya_yuksekligi = fields.Integer(string="Mahya Yük. (m)", required=True, tracking=True)
    makas_araligi = fields.Integer(string="Makas Aralığı (m)", required=True, tracking=True)
    es_kumes_sayisi = fields.Integer(string="Eş Kümes Sayısı", required=True, tracking=True)
    durum = fields.Selection([("Taslak", "Taslak"), ("Kesinleşti", "Kesinleşti")], string="Teklif Durumu", default="Taslak", required=True, tracking=True)

    # Yemlik Hattı
    yh_hat_sayisi = fields.Integer(string="Hat Sayısı", required=True, tracking=True)
    yh_ara_durdurucu = fields.Selection([("Var", "Var"), ("Yok", "Yok")], default="Yok", string="Ara Durdurucu", required=True, tracking=True)
    yh_kazan_tipi = fields.Many2one("product.template", "Kazan Tipi", required=True, domain="[('product_tag_ids.name', '=', 'yh_kazan_tipi')]", tracking=True)
    yh_yemlik_tipi = fields.Many2one("product.template", "Yemlik Tipi", required=True, domain="[('product_tag_ids.name', '=', 'yh_yemlik_tipi')]", tracking=True)
    yh_yem_motoru = fields.Many2one("product.template", "Yem Motoru", required=True, domain="[('product_tag_ids.name', '=', 'yh_yem_motoru')]", tracking=True)
    yh_civciv_yemlik_sehpa = fields.Integer(string="Civciv Yem./Seh.", required=True)

    # Sulama Hattı
    sh_hat_sayisi = fields.Integer(string="Hat Sayısı", required=True, tracking=True)
    sh_regulator_tipi = fields.Many2one("product.template", "Regülatör Tipi", required=True, domain="[('product_tag_ids.name', '=', 'sh_regulator_tipi')]", tracking=True)
    sh_hat_bolum_sayisi = fields.Integer(string="Hat Bölüm Sayısı", required=True, tracking=True)
    sh_medikator = fields.Selection([("Var", "Var"), ("Yok", "Yok")], default="Yok", string="Medikatör", required=True, tracking=True)
    sh_nipel_tipi = fields.Many2one("product.template", "Nipel Tipi", required=True, domain="[('product_tag_ids.name', '=', 'sh_nipel_tipi')]", tracking=True)
    sh_civciv_suluk_sehpa = fields.Integer(string="Civciv Sul./Seh.", required=True, tracking=True)

    # Yemlik Kaldırma
    yk_tipi = fields.Selection([("Manuel", "Manuel"), ("Otomatik", "Otomatik")], default="Otomatik", string="Tipi", required=True, tracking=True)
    yk_vinc_tipi = fields.Many2one("product.template", "Vinç Tipi", required=False, domain="[('product_tag_ids.name', '=', 'yk_vinc_tipi')]", tracking=True)
    yk_motor_sayisi = fields.Integer(string="Motor Sayısı", required=True, tracking=True, compute="_yk_motor_sayisi_hesapla", readonly=False, store=True)

    # Sulama Kaldırma
    sk_tipi = fields.Selection([("Manuel", "Manuel"), ("Otomatik", "Otomatik")], default="Otomatik", string="Tipi", required=True, tracking=True)
    sk_vinc_tipi = fields.Many2one("product.template", "Vinç Tipi", required=False, domain="[('product_tag_ids.name', '=', 'sk_vinc_tipi')]", tracking=True)
    sk_motor_sayisi = fields.Integer(string="Motor Sayısı", required=True, tracking=True, compute="_sk_motor_sayisi_hesapla", readonly=False, store=True)

    # Havalandırma
    hv_klepe_tipi = fields.Many2one("product.template", "Klepe Tipi", required=True, domain="[('product_tag_ids.name', '=', 'hv_klepe_tipi')]", tracking=True)
    hv_klepe_sayisi = fields.Integer(string="Klepe Sayısı", required=True, tracking=True)
    hv_klepe_ac_kap = fields.Selection([("Var", "Var"), ("Yok", "Yok")], default="Yok", string="Klepe Aç./Ka.", required=True, tracking=True)
    hv_klepe_davlumbaz = fields.Selection([("Var", "Var"), ("Yok", "Yok")], default="Yok", string="Klepe Davlumbaz", required=True, tracking=True)
    hv_tunel_fan = fields.Many2one("product.template", "Tünel Fan", required=True, domain="[('product_tag_ids.name', '=', 'hv_tunel_fan')]", tracking=True)
    hv_tunel_fan_sayisi = fields.Integer(string="Tünel Fan Sayısı", required=True, tracking=True)
    hv_mini_fan = fields.Many2one("product.template", "Mini Fan", required=True, domain="[('product_tag_ids.name', '=', 'hv_mini_fan')]", tracking=True)
    hv_mini_fan_sayisi = fields.Integer(string="Mini Fan Sayısı", required=True, tracking=True)
    hv_konik_fan = fields.Many2one("product.template", "Konik Fan", required=True, domain="[('product_tag_ids.name', '=', 'hv_konik_fan')]", tracking=True)
    hv_konik_fan_sayisi = fields.Integer(string="Konik Fan Sayısı", required=True, tracking=True)

    # Pedler
    teklif_pedleri = fields.One2many('teklif.ped', 'teklif_id', string='Teklif Ped Kayıtları')

    # Silolar
    teklif_silolari = fields.One2many('teklif.silo', 'teklif_id', string='Teklif Silo Kayıtları')

    # Ürünler
    teklif_urunleri = fields.One2many('teklif.urun', 'teklif_id', string='Teklif Ürün Kayıtları')

    # Yem Nakil
    yn_motor_tipi = fields.Many2one("product.template", "Motor Tipi", required=True, domain="[('product_tag_ids.name', '=', 'yn_motor_tipi')]", tracking=True)
    yn_tekli_cikis_sayisi = fields.Integer(string="Tekli Çıkış Sayısı", required=True, tracking=True)
    yn_tekli_cikis_baglanti = fields.Selection([("Normal", "Normal"), ("Tandem", "Tandem")], default="Normal", string="Tekli Çıkış Bağlantı", required=True, tracking=True)
    yn_ciftli_cikis_sayisi = fields.Integer(string="Çiftli Çıkış Sayısı", required=True, tracking=True)
    yn_ciftli_cikis_baglanti = fields.Selection([("Normal", "Normal"), ("Tandem", "Tandem")], default="Normal", string="Çiftli Çıkış Bağlantı", required=True, tracking=True)

    # Aydınlatma
    ay_turu = fields.Selection([("Led Ampül Beyaz", "Led Ampül Beyaz"), ("Led Ampül Günışığı", "Led Ampül Günışığı"), ("Led Bar Beyaz", "Led Bar Beyaz"), ("Led Bar Günışığı", "Led Bar Günışığı")], default="Led Ampül Beyaz", string="Türü", required=True, tracking=True)
    ay_hat_sayisi = fields.Integer(string="Hat Sayısı", required=True, tracking=True)
    ay_lamba_araligi = fields.Selection([("3 metre", "3 metre"), ("4 metre", "4 metre")], default="3 metre", string="Lamba Aralığı (m)", required=True, tracking=True)

    # Pano
    pn_maliyet = fields.Float(string="Pan. Maliyeti (TRY)", required=True, tracking=True)

    # Isıtma
    is_miktar = fields.Integer(string="Miktar", required=True, tracking=True)
    is_maliyet = fields.Float(string="Maliyet (TRY)", required=True, tracking=True)
    is_urun = fields.Many2one("product.template", "Ürün", required=True, domain="[('product_tag_ids.name', '=', 'is_urun')]", tracking=True)

    @api.depends('sk_tipi', 'yh_hat_sayisi', 'kumes_uzunluk', 'ortadan_bolme')
    def _sk_motor_sayisi_hesapla(self):
        val = 0
        if self.sk_tipi == "Otomatik":
            val = self.yh_hat_sayisi * self.kumes_uzunluk
            if val < 400:
                val = 1
            if val >= 300:
                val = 2
            if self.ortadan_bolme == "Evet":
                val = val * 2

        self.sk_motor_sayisi = val

    @api.depends('yk_tipi', 'yh_hat_sayisi', 'kumes_uzunluk', 'ortadan_bolme')
    def _yk_motor_sayisi_hesapla(self):
        val = 0
        if self.yk_tipi == "Otomatik":
            val = self.yh_hat_sayisi * self.kumes_uzunluk
            if val < 380:
                val = 1
            if val >= 300:
                val = 2
            if self.ortadan_bolme == "Evet":
                val = val * 2

        self.yk_motor_sayisi = val

    def action_generate_order(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.musteri_id.id,
            'validity_date': self.gecerlilik_tarihi
        })

        for data in self.teklif_urunleri:
            self.env['sale.order.line'].create({
                'product_template_id': data['tu_urun'].id,
                'product_id': data['tu_urun'].product_variant_id.id,
                'order_id': sale_order.id,
                'name': data['tu_urun'].name,
                'product_uom_qty': data['tu_miktar'],
                'price_unit': data['tu_maliyet']
            })

    def action_generate_products(self):
        # Ürün tablosu siliniyor.
        for rec in self:
            rec.write({'teklif_urunleri': [(5, 0, 0)]})

        urun_line = []
        if self.kumes_tipi == "Broyler":
            if self.yh_hat_sayisi > 0:
                urun_line.append([0, 0, {
                    'tu_urun': self.yh_kazan_tipi.id,
                    'tu_miktar': self.yh_hat_sayisi,
                    'tu_maliyet': self.yh_kazan_tipi.list_price,
                    'tu_maliyet_toplam': self.yh_hat_sayisi*self.yh_kazan_tipi.list_price
                }])
                urun_line.append([0, 0, {
                    'tu_urun': self.yh_yem_motoru.id,
                    'tu_miktar': self.yh_hat_sayisi,
                    'tu_maliyet': self.yh_yem_motoru.list_price,
                    'tu_maliyet_toplam': self.yh_hat_sayisi*self.yh_yem_motoru.list_price
                }])

                # Motor Mili
                barcode = ''
                if self.yh_kazan_tipi.barcode == '3.YM.100.000.000':  # 90kg yem kazanı
                    barcode = '3.YM.104.000.000'  # Kısa

                if self.yh_kazan_tipi.barcode == '3.YM.101.000.000':  # 120kg yem kazanı
                    barcode = '3.YM.106.000.000'  # Orta

                if self.yh_kazan_tipi.barcode == '3.YM.102.000.000':  # 150kg yem kazanı
                    barcode = '3.YM.105.000.000'  # Uzun

                product = self.env['product.template'].search([('barcode', '=', barcode)], limit=1)
                if product:
                    urun_line.append([0, 0, {
                        'tu_urun': product.id,
                        'tu_miktar': self.yh_hat_sayisi,
                        'tu_maliyet': product.list_price,
                        'tu_maliyet_toplam': self.yh_hat_sayisi*product.list_price
                    }])

                # Yemlik Hat Sonu
                product_yhs = self.env['product.template'].search([('barcode', '=', '3.YM.107.000.000')], limit=1)
                if product_yhs:
                    urun_line.append([0, 0, {
                        'tu_urun': product_yhs.id,
                        'tu_miktar': self.yh_hat_sayisi,
                        'tu_maliyet': product_yhs.list_price,
                        'tu_maliyet_toplam': self.yh_hat_sayisi * product_yhs.list_price
                    }])

                # Ara Durdurucu
                if self.yh_ara_durdurucu == 'Var':
                    product_ad = self.env['product.template'].search([('barcode', '=', '3.YM.108.000.000')], limit=1)
                    if product_ad:
                        urun_line.append([0, 0, {
                            'tu_urun': product_ad.id,
                            'tu_miktar': self.yh_hat_sayisi,
                            'tu_maliyet': product_ad.list_price,
                            'tu_maliyet_toplam': self.yh_hat_sayisi * product_ad.list_price
                        }])

                # 45mm Yemlik Borusu, Kelepçesi ve Yayı
                product_yb = self.env['product.template'].search([('barcode', '=', '3.YM.110.000.000')], limit=1)
                product_ybk = self.env['product.template'].search([('barcode', '=', '3.YM.103.000.000')], limit=1)
                product_yy = self.env['product.template'].search([('barcode', '=', '1.YY.001.001.001')], limit=1)
                if product_yb:
                    urun_line.append([0, 0, {
                        'tu_urun': product_yb.id,
                        'tu_miktar': self.yh_hat_sayisi*self.kumes_uzunluk,
                        'tu_maliyet': product_yb.list_price,
                        'tu_maliyet_toplam': self.yh_hat_sayisi * self.kumes_uzunluk * product_yb.list_price
                    }])

                if product_ybk:
                    urun_line.append([0, 0, {
                        'tu_urun': product_ybk.id,
                        'tu_miktar': (ceil(self.kumes_uzunluk/3)+1)*self.yh_hat_sayisi,
                        'tu_maliyet': product_ybk.list_price,
                        'tu_maliyet_toplam': (ceil(self.kumes_uzunluk/3)+1)*self.yh_hat_sayisi * product_ybk.list_price
                    }])

                if product_yy:
                    urun_line.append([0, 0, {
                        'tu_urun': product_yy.id,
                        'tu_miktar': self.yh_hat_sayisi*self.kumes_uzunluk,
                        'tu_maliyet': product_yy.list_price,
                        'tu_maliyet_toplam': self.yh_hat_sayisi*self.kumes_uzunluk * product_yy.list_price
                    }])

                # Yemlikler
                urun_line.append([0, 0, {
                    'tu_urun': self.yh_yemlik_tipi.id,
                    'tu_miktar': ceil(self.kumes_uzunluk/0.75)*self.yh_hat_sayisi,
                    'tu_maliyet': self.yh_yemlik_tipi.list_price,
                    'tu_maliyet_toplam': ceil(self.kumes_uzunluk/0.75)*self.yh_hat_sayisi * self.yh_yemlik_tipi.list_price
                }])

                # Civciv Yemlik, Sehpa
                if self.yh_civciv_yemlik_sehpa > 0:
                    product_cy = self.env['product.template'].search([('barcode', '=', '3.YM.004.000.000')], limit=1)
                    product_cs = self.env['product.template'].search([('barcode', '=', '3.YM.006.000.000')], limit=1)
                    if product_cy:
                        urun_line.append([0, 0, {
                            'tu_urun': product_cy.id,
                            'tu_miktar': self.yh_civciv_yemlik_sehpa,
                            'tu_maliyet': product_cy.list_price,
                            'tu_maliyet_toplam': self.yh_civciv_yemlik_sehpa * product_cy.list_price
                        }])

                    if product_cs:
                        urun_line.append([0, 0, {
                            'tu_urun': product_cs.id,
                            'tu_miktar': self.yh_civciv_yemlik_sehpa + self.sh_civciv_suluk_sehpa,
                            'tu_maliyet': product_cs.list_price,
                            'tu_maliyet_toplam': (self.yh_civciv_yemlik_sehpa + self.sh_civciv_suluk_sehpa) * product_cs.list_price
                        }])

            if self.sh_hat_sayisi > 0:
                # Nipel Tipi
                urun_line.append([0, 0, {
                    'tu_urun': self.sh_nipel_tipi.id,
                    'tu_miktar': self.sh_hat_sayisi*self.kumes_uzunluk,
                    'tu_maliyet': self.sh_nipel_tipi.list_price,
                    'tu_maliyet_toplam': self.sh_hat_sayisi*self.kumes_uzunluk * self.sh_nipel_tipi.list_price
                }])

                # Nipel Taşıyıcı Boru
                product_ntb = self.env['product.template'].search([('barcode', '=', '3.SM.015.000.000')], limit=1)
                if product_ntb:
                    urun_line.append([0, 0, {
                        'tu_urun': product_ntb.id,
                        'tu_miktar': self.sh_hat_sayisi*self.kumes_uzunluk,
                        'tu_maliyet': product_ntb.list_price,
                        'tu_maliyet_toplam': self.sh_hat_sayisi*self.kumes_uzunluk * product_ntb.list_price
                    }])

                # Nipel Çanak
                product_nc = self.env['product.template'].search([('barcode', '=', '3.SM.003.000.000')], limit=1)
                if product_nc:
                    urun_line.append([0, 0, {
                        'tu_urun': product_nc.id,
                        'tu_miktar': ceil(self.kumes_uzunluk/0.2)*self.sh_hat_sayisi,
                        'tu_maliyet': product_nc.list_price,
                        'tu_maliyet_toplam': ceil(self.kumes_uzunluk/0.2)*self.sh_hat_sayisi * product_nc.list_price
                    }])

                # Nipel Ek Muf Takım
                product_nemf = self.env['product.template'].search([('barcode', '=', '3.SM.009.000.000')], limit=1)
                if product_nemf:
                    urun_line.append([0, 0, {
                        'tu_urun': product_nemf.id,
                        'tu_miktar': (ceil(self.kumes_uzunluk / 4) + 1) * self.sh_hat_sayisi,
                        'tu_maliyet': product_nemf.list_price,
                        'tu_maliyet_toplam': (ceil(self.kumes_uzunluk / 4) + 1) * self.sh_hat_sayisi * product_nemf.list_price
                    }])

                # Regülatör Tipi
                urun_line.append([0, 0, {
                    'tu_urun': self.sh_regulator_tipi.id,
                    'tu_miktar': self.sh_hat_sayisi * self.sh_hat_bolum_sayisi,
                    'tu_maliyet': self.sh_regulator_tipi.list_price,
                    'tu_maliyet_toplam': self.sh_hat_sayisi * self.sh_hat_bolum_sayisi * self.sh_regulator_tipi.list_price
                }])

                # Basınç Regülatör Hat Sonu
                product_bghs = self.env['product.template'].search([('barcode', '=', '3.SM.014.000.000')], limit=1)
                if product_bghs:
                    urun_line.append([0, 0, {
                        'tu_urun': product_bghs.id,
                        'tu_miktar': self.sh_hat_sayisi * self.sh_hat_bolum_sayisi,
                        'tu_maliyet': product_bghs.list_price,
                        'tu_maliyet_toplam': self.sh_hat_sayisi * self.sh_hat_bolum_sayisi * product_bghs.list_price
                    }])

                if self.sh_civciv_suluk_sehpa > 0:
                    # Civciv Suluk
                    product_cs = self.env['product.template'].search([('barcode', '=', '3.SM.001.000.000')], limit=1)
                    if product_cs:
                        urun_line.append([0, 0, {
                            'tu_urun': product_cs.id,
                            'tu_miktar': self.sh_civciv_suluk_sehpa,
                            'tu_maliyet': product_cs.list_price,
                            'tu_maliyet_toplam': self.sh_civciv_suluk_sehpa * product_cs.list_price
                        }])

                if self.sh_medikator == 'Var':
                    # Medikatör
                    product_mdk = self.env['product.template'].search([('barcode', '=', '3.SM.008.000.000')], limit=1)
                    if product_mdk:
                        urun_line.append([0, 0, {
                            'tu_urun': product_mdk.id,
                            'tu_miktar': self.es_kumes_sayisi,
                            'tu_maliyet': product_mdk.list_price,
                            'tu_maliyet_toplam': self.es_kumes_sayisi * product_mdk.list_price
                        }])

            self.write({'teklif_urunleri': urun_line})


class TeklifPed(models.Model):
    _name = "teklif.ped"
    _inherit = ['mail.thread']
    _description = "Teklif Sihirbazı teklifler için ped kayıtları"

    ped_no = fields.Integer(string="No", required=True, tracking=True)
    ped_tipi = fields.Selection([("Kasalı", "Kasalı"), ("Havuzlu", "Havuzlu")], default="Kasalı", string="Ped Tipi", required=True, tracking=True)
    ped_kagit_markasi = fields.Selection([("Tabreed", "Tabreed"), ("Munters", "Munters"), ("Alindair", "Alindair")], string="Kağıt Markası", default="Tabreed", required=True, tracking=True)
    ped_kagit_eni = fields.Selection([("10 cm", "10 cm"), ("15 cm", "15 cm")], default="10 cm", string="Kağıt Eni", required=True, tracking=True)
    ped_yuksekligi = fields.Selection([("100 cm", "100 cm"), ("120 cm", "120 cm"), ("150 cm", "150 cm"), ("180 cm", "180 cm"), ("200 cm", "200 cm")], default="100 cm", string="Ped Yüksekliği", required=True, tracking=True)
    ped_modul_uzunlugu = fields.Integer(string="Ped Modül Uzunluğu (m)", required=True, tracking=True)
    ped_kapak_sistemi = fields.Selection([("Var", "Var"), ("Yok", "Yok")], default="Yok", string="Kapak Sistemi", required=True, tracking=True)
    ped_acma_kapama = fields.Selection([("Var", "Var"), ("Yok", "Yok")], default="Yok", string="Açma/Kapama", required=True, tracking=True)
    teklif_id = fields.Many2one('teklif', string='Teklif ID', tracking=True)

    @api.onchange('ped_modul_uzunlugu')
    def _onchange_ped_modul_uzunlugu(self):
        val = self.ped_modul_uzunlugu % 3
        if val != 0:
            self.ped_modul_uzunlugu += (3 - val)


class TeklifSilo(models.Model):
    _name = "teklif.silo"
    _inherit = ['mail.thread']
    _description = "Teklif Sihirbazı teklifler için silo kayıtları"

    silo_no = fields.Integer(string="No", required=True, tracking=True)
    silo_urun = fields.Many2one("product.template", "Ürün", required=True, domain="[('product_tag_ids.name', '=', 'silo_urun')]", tracking=True)
    teklif_id = fields.Many2one('teklif', string='Teklif ID', tracking=True)


class TeklifUrun(models.Model):
    _name = "teklif.urun"
    _inherit = ['mail.thread']
    _description = "Teklif Sihirbazı teklifler için ürün kayıtları"

    tu_urun = fields.Many2one("product.template", "Ürün", required=True, tracking=True)
    tu_miktar = fields.Integer(string="Miktar", required=True, tracking=True)
    tu_maliyet = fields.Float(string="Birim Fiyat", required=True, tracking=True)
    tu_maliyet_toplam = fields.Float(string="Toplam", required=True, tracking=True, readonly=True)
    teklif_id = fields.Many2one('teklif', string='Teklif ID', tracking=True)

    @api.onchange('tu_miktar')
    def _onchange_tu_miktar(self):
        self.tu_maliyet_toplam = self.tu_miktar*self.tu_maliyet

    @api.onchange('tu_maliyet')
    def _onchange_tu_maliyet(self):
        self.tu_maliyet_toplam = self.tu_miktar * self.tu_maliyet
