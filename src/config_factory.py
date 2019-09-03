from lib.model import *
import site_config as C # config

def load(prod = False):
    page = PageConfig()
    page.title = C.page_title
    page.description = C.page_description

    site = SiteConfig()
    site.languages = C.site_languages
    site.url = C.site_url
    site.enable_ga = C.site_enable_ga
    site.page_config = page

    generator = GeneratorConfig()
    generator.cache_dir = C.generator_cache_dir
    generator.out_dir = C.generator_out_dir
    generator.site_config = site
    
    if prod:
        generator.out_dir = C.prod_generator_out_dir
        site.url = C.prod_site_url
        site.enable_ga = C.prod_site_enable_ga

    return generator
