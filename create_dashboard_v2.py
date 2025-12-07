#!/usr/bin/env python3
"""
MIDOR-ETHYDCO Integration Dashboard V2
Modern, stunning design with language toggle
Includes ETHYDCO Knowledge Base tab
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# ============================================================================
# CONSTANTS
# ============================================================================

OPERATING_HOURS_PER_YEAR = 8000

# ============================================================================
# ETHYDCO DATA STRUCTURE
# ============================================================================

def load_ethydco_data():
    """Load ETHYDCO questionnaire data."""
    return {
        'company_info': {
            'name': 'ETHYDCO',
            'name_ar': 'إيثيدكو',
            'full_name': 'Egyptian Ethylene & Derivatives Company',
            'full_name_ar': 'الشركة المصرية للإيثيلين ومشتقاته',
            'scope': 'Polyethylene Production "Petrochemicals"',
            'scope_ar': 'إنتاج البولي إيثيلين "البتروكيماويات"'
        },

        'feeds': [
            {
                'id': 'feed_main',
                'name': 'Feed',
                'name_ar': 'التغذية',
                'category': 'feeds',
                'design_value': 81.3,
                'design_unit': 'T/hr',
                'actual_value': {'min': 65, 'max': 70},
                'actual_unit': 'T/hr',
                'data_source': 'Material Balance',
                'comment': 'Gap is (11-16) T/hr to design capacity',
                'comment_ar': 'الفجوة (11-16) طن/ساعة عن السعة التصميمية',
                'routing': {
                    'source': 'GASCO Pipeline',
                    'source_ar': 'خط أنابيب جاسكو',
                    'destination': 'Steam Crackers (via Purification)',
                    'destination_ar': 'التكسير البخاري (عبر التنقية)'
                }
            },
            {
                'id': 'feed_composition',
                'name': 'Feed Composition',
                'name_ar': 'تركيب التغذية',
                'category': 'feeds',
                'description': 'Feed to Crackers is a mixture of Ethane & Propane',
                'description_ar': 'التغذية للتكسير هي خليط من الإيثان والبروبان',
                'composition': {'C2 (Ethane)': 95, 'C3 (Propane)': 5},
                'composition_unit': 'wt%',
                'data_source': 'Material Balance',
                'comment': 'Propane content range in feed is (5-15) wt%',
                'comment_ar': 'نسبة البروبان في التغذية (5-15) وزني%'
            },
            {
                'id': 'feed_impurities',
                'name': 'Feed Impurities',
                'name_ar': 'شوائب التغذية',
                'category': 'feeds',
                'fresh_feed': {
                    'CO2': {'value': 17.0, 'unit': 'mol%'},
                    'H2S': {'value': 100, 'unit': 'ppm mol'},
                    'Hg': {'value': 140, 'unit': 'ppb wt'}
                },
                'treated_feed': {
                    'CO2': {'value': '<100', 'unit': 'ppmw'},
                    'H2S': 'zero',
                    'Hg': 'zero'
                },
                'data_source': 'Material Balance',
                'comment': 'Fresh feed from GASCO is treated in purification units to remove CO2, H2S, Hg before cracking',
                'comment_ar': 'تتم معالجة التغذية من جاسكو في وحدات التنقية لإزالة الشوائب قبل التكسير'
            },
            {
                'id': 'feed_limitations',
                'name': 'Feed Limitations',
                'name_ar': 'قيود التغذية',
                'category': 'feeds',
                'limitations': [
                    'C4+ is not permitted in the feed',
                    'Vapor phase only',
                    'P (min) = 8 kg/cm²g',
                    'T = ambient'
                ],
                'limitations_ar': [
                    'لا يُسمح بوجود C4+ في التغذية',
                    'طور بخاري فقط',
                    'الضغط (أدنى) = 8 كجم/سم² مقياس',
                    'درجة الحرارة = محيطة'
                ],
                'conditions': {
                    'pressure': {'min': 8, 'unit': 'kg/cm²g'},
                    'temperature': 'ambient',
                    'phase': 'Vapor'
                },
                'data_source': 'Material Balance'
            }
        ],

        'products': [
            {
                'id': 'ethylene_polymer',
                'name': 'Ethylene Polymer Grade',
                'name_ar': 'إيثيلين درجة البوليمر',
                'category': 'products',
                'design_value': 460000,
                'design_unit': 'T/Year',
                'actual_value': None,
                'data_source': 'Material Balance',
                'comment': 'A feedstock for Polyethylene production',
                'comment_ar': 'مادة خام لإنتاج البولي إيثيلين',
                'definition_key': 'ethylene',
                'routing': {
                    'source': 'Ethylene Fractionator',
                    'source_ar': 'مجزئ الإيثيلين',
                    'destination': 'Polyethylene Plant',
                    'destination_ar': 'مصنع البولي إيثيلين'
                }
            },
            {
                'id': 'h2_offgas',
                'name': 'H2 Offgas',
                'name_ar': 'غاز الهيدروجين',
                'category': 'products',
                'design_value': 6.812,
                'design_unit': 'T/hr',
                'actual_value': {'min': 4, 'max': 4.5},
                'actual_unit': 'T/hr',
                'composition': {
                    'H2': {'min': 87, 'max': 90},
                    'CO': 0.27,
                    'CH4': {'min': 8.5, 'max': 11.5},
                    'C2H4': 0.25
                },
                'composition_unit': 'mol%',
                'conditions': {'P': 3, 'P_unit': 'kg/cm²g', 'T': 39, 'T_unit': '°C'},
                'data_source': 'Material Balance',
                'definition_key': 'h2_offgas',
                'routing': {
                    'source': 'Cold Box / PSA',
                    'source_ar': 'الصندوق البارد',
                    'destination': 'Fuel Gas Mixing Drum',
                    'destination_ar': 'خلاط غاز الوقود'
                }
            },
            {
                'id': 'methane_offgas',
                'name': 'Methane Offgas',
                'name_ar': 'غاز الميثان',
                'category': 'products',
                'design_value': {'min': 4.5, 'max': 6.2},
                'design_unit': 'T/hr',
                'actual_value': {'min': 3, 'max': 4.5},
                'actual_unit': 'T/hr',
                'composition': {
                    'CH4': {'min': 76, 'max': 82.5},
                    'H2': {'min': 17, 'max': 22},
                    'CO': 0.3
                },
                'composition_unit': 'mol%',
                'conditions': {'P': 3.2, 'P_unit': 'kg/cm²g', 'T': 24.5, 'T_unit': '°C'},
                'data_source': 'Material Balance',
                'definition_key': 'methane_offgas',
                'routing': {
                    'source': 'Demethanizer Overhead',
                    'source_ar': 'أعلى عمود الميثان',
                    'destination': 'Fuel Gas Mixing Drum',
                    'destination_ar': 'خلاط غاز الوقود'
                }
            },
            {
                'id': 'c3_stream',
                'name': 'C3s Stream (De-C3 Overhead)',
                'name_ar': 'تيار C3 (أعلى عمود إزالة البروبان)',
                'category': 'products',
                'design_value': {'min': 2.9, 'max': 4.3},
                'design_unit': 'T/hr',
                'actual_value': {'min': 2, 'max': 3},
                'actual_unit': 'T/hr',
                'composition': {
                    'Propylene': {'min': 69.5, 'max': 74},
                    'Propane': {'min': 24, 'max': 28},
                    'C2s': 0.18,
                    'Propyne': 3
                },
                'composition_unit': 'mol%',
                'conditions': {'P': 32, 'P_unit': 'kg/cm²g', 'T': -1, 'T_unit': '°C'},
                'data_source': 'Material Balance',
                'definition_key': 'propylene',
                'routing': {
                    'source': 'De-C3 Column Overhead',
                    'source_ar': 'أعلى عمود C3',
                    'destination': 'Fuel Gas / LPG Export',
                    'destination_ar': 'غاز الوقود / تصدير الغاز المسال'
                }
            },
            {
                'id': 'c4_stream',
                'name': 'C4s Stream',
                'name_ar': 'تيار C4 (البيوتان)',
                'category': 'products',
                'design_value': 0.9,
                'design_unit': 'T/hr',
                'actual_value': 0.7,
                'actual_unit': 'T/hr',
                'composition': {
                    'n-Butane': {'min': 37, 'max': 50},
                    'Butene-1': {'min': 23, 'max': 30},
                    'Butene-2': {'min': 18, 'max': 21}
                },
                'composition_unit': 'mol%',
                'conditions': {'P': 31, 'P_unit': 'kg/cm²g', 'T': 41, 'T_unit': '°C'},
                'data_source': 'Material Balance',
                'definition_key': 'lpg',
                'routing': {
                    'source': 'De-C4 Column',
                    'source_ar': 'عمود C4',
                    'destination': 'Butadiene Unit / LPG Export',
                    'destination_ar': 'وحدة البيوتادايين / التصدير'
                }
            },
            {
                'id': 'butadiene',
                'name': '1,3 Butadiene',
                'name_ar': 'البيوتادايين 1,3',
                'category': 'products',
                'design_value': 20000,
                'design_unit': 'T/Year',
                'actual_value': None,
                'data_source': 'Material Balance',
                'definition_key': 'butadiene',
                'routing': {
                    'source': 'Butadiene Extraction Unit',
                    'source_ar': 'وحدة استخلاص البيوتادايين',
                    'destination': 'Export / SBR Production',
                    'destination_ar': 'تصدير / إنتاج المطاط'
                }
            },
            {
                'id': 'pygas',
                'name': 'Pyrolysis Gasoline',
                'name_ar': 'بنزين التكسير',
                'category': 'products',
                'design_value': {'min': 100, 'max': 400},
                'design_unit': 'Kg/hr',
                'actual_value': {'min': 70, 'max': 250},
                'actual_unit': 'Kg/hr',
                'composition': {
                    'Toluene/Xylene/EB': 3.5,
                    'C9-204°C': 48,
                    'Styrene': 23,
                    'PGO (204-288°C)': 20
                },
                'composition_unit': 'mol%',
                'comment': 'PG from quench tower',
                'comment_ar': 'بنزين التكسير من برج التبريد',
                'data_source': 'Material Balance',
                'definition_key': 'pyrolysis_gasoline',
                'routing': {
                    'source': 'Quench Tower Bottoms',
                    'source_ar': 'قاع برج التبريد',
                    'destination': 'Fuel System / Gasoline Blending',
                    'destination_ar': 'نظام الوقود / مزج البنزين'
                }
            }
        ],

        'flared_gases': [
            {
                'id': 'ethylene_flare',
                'name': 'Ethylene Plant Flare',
                'name_ar': 'شعلة مصنع الإيثيلين',
                'category': 'flares',
                'flare_type': 'Steam assisted flare',
                'flare_type_ar': 'شعلة مساعدة بالبخار',
                'flow': 'Non-routine flaring',
                'flow_ar': 'حرق غير روتيني',
                'comment': 'Flaring just in cases of upsets and S/D, not measured',
                'comment_ar': 'الحرق فقط في حالات الاضطرابات والإيقاف، غير مقاس',
                'is_measured': False,
                'routing': {
                    'source': 'Ethylene Plant Emergency Relief',
                    'source_ar': 'تصريف طوارئ مصنع الإيثيلين',
                    'destination': 'Atmosphere (combusted)',
                    'destination_ar': 'الجو (محترق)'
                }
            },
            {
                'id': 'pe_flare',
                'name': 'Polyethylene Plant Flare',
                'name_ar': 'شعلة مصنع البولي إيثيلين',
                'category': 'flares',
                'flare_type': 'Steam assisted flare',
                'flare_type_ar': 'شعلة مساعدة بالبخار',
                'flow': 'Non-routine flaring',
                'flow_ar': 'حرق غير روتيني',
                'comment': 'Flaring just in cases of upsets, startup and S/D, not measured',
                'comment_ar': 'الحرق فقط في حالات الاضطرابات والتشغيل والإيقاف، غير مقاس',
                'is_measured': False,
                'routing': {
                    'source': 'PE Plant Emergency Relief',
                    'source_ar': 'تصريف طوارئ مصنع البولي إيثيلين',
                    'destination': 'Atmosphere (combusted)',
                    'destination_ar': 'الجو (محترق)'
                }
            }
        ],

        'fuel_gas': [
            {
                'id': 'internal_offgas',
                'name': 'Internal Offgases',
                'name_ar': 'الغازات الداخلية',
                'category': 'fuel',
                'design_value': {'min': 11.314, 'max': 13.722},
                'design_unit': 'T/hr',
                'actual_value': {'min': 7.9, 'max': 9.6},
                'actual_unit': 'T/hr',
                'composition': {
                    'H2': {'min': 75, 'max': 80},
                    'CH4': {'min': 19, 'max': 24},
                    'HCs': 0.5
                },
                'composition_unit': 'mol%',
                'conditions': {'P': 3.2, 'P_unit': 'kg/cm²g', 'T': 36, 'T_unit': '°C'},
                'data_source': 'Material Balance',
                'comment': 'All offgas streams are mixed and used inside the fuel system. Ethydco imports natural gas in case of shortage.',
                'comment_ar': 'جميع تيارات الغاز المتبقي تُخلط وتُستخدم في نظام الوقود. تستورد إيثيدكو الغاز الطبيعي عند النقص.',
                'routing': {
                    'source': 'H2 + CH4 Offgas Streams',
                    'source_ar': 'تيارات H2 + CH4',
                    'destination': 'Fuel Gas Mixing Drum → Furnaces',
                    'destination_ar': 'خلاط الوقود → الأفران'
                }
            },
            {
                'id': 'natural_gas_import',
                'name': 'Natural Gas (from GASCO)',
                'name_ar': 'الغاز الطبيعي (من جاسكو)',
                'category': 'fuel',
                'design_value': None,
                'actual_value': '8170 Ton (total imported since start of 2025)',
                'actual_value_ar': '8170 طن (إجمالي المستورد منذ بداية 2025)',
                'data_source': 'Measured',
                'comment': 'Variable flow rate based on demand, imported in case of shortage in generated offgases',
                'comment_ar': 'معدل تدفق متغير حسب الطلب، يُستورد عند نقص الغازات المولدة داخلياً',
                'routing': {
                    'source': 'GASCO Pipeline',
                    'source_ar': 'خط أنابيب جاسكو',
                    'destination': 'Fuel Gas Mixing Drum',
                    'destination_ar': 'خلاط غاز الوقود'
                }
            },
            {
                'id': 'pygas_fuel',
                'name': 'Pyrolysis Gasoline (as fuel)',
                'name_ar': 'بنزين التكسير (كوقود)',
                'category': 'fuel',
                'design_value': {'min': 92, 'max': 393},
                'design_unit': 'Kg/hr',
                'actual_value': {'min': 64, 'max': 275},
                'actual_unit': 'Kg/hr',
                'composition': {
                    'Toluene/Xylene/EB': 3.5,
                    'C9-204°C': 48,
                    'Styrene': 23,
                    'PGO (204-288°C)': 20
                },
                'composition_unit': 'mol%',
                'conditions': {'P': 0.97, 'P_unit': 'kg/cm²g', 'T': 80, 'T_unit': '°C'},
                'data_source': 'Material Balance',
                'routing': {
                    'source': 'Quench Tower',
                    'source_ar': 'برج التبريد',
                    'destination': 'Fuel System / Fired Heaters',
                    'destination_ar': 'نظام الوقود / السخانات'
                }
            }
        ],

        'other_gases': [
            {
                'id': 'amine_stripper',
                'name': 'Amine Stripper Offgas',
                'name_ar': 'غاز منزع الأمين',
                'category': 'other',
                'design_value': 23.2,
                'design_unit': 'T/hr',
                'actual_value': {'min': 16, 'max': 18},
                'actual_unit': 'T/hr',
                'composition': {
                    'Ethane': 0.19,
                    'CO2': 90,
                    'H2S': 0.05,
                    'Steam': 9
                },
                'composition_unit': 'mol%',
                'conditions': {'P': 0.57, 'P_unit': 'kg/cm²g', 'T': 57, 'T_unit': '°C'},
                'data_source': 'Material Balance',
                'comment': 'CO2-rich stream directed to incinerator to burn H2S and HCs before releasing to atmosphere',
                'comment_ar': 'تيار غني بـ CO2 يُوجه للمحرقة لحرق H2S والهيدروكربونات قبل الإطلاق للجو',
                'definition_key': 'amine_stripper',
                'routing': {
                    'source': 'Amine Regeneration Unit',
                    'source_ar': 'وحدة تجديد الأمين',
                    'destination': 'Incinerator → Atmosphere',
                    'destination_ar': 'المحرقة → الجو'
                }
            }
        ]
    }


# ============================================================================
# DEFINITIONS DATABASE
# ============================================================================

DEFINITIONS = {
    'ethylene': {
        'term': 'Ethylene',
        'term_ar': 'الإيثيلين',
        'simple': 'Basic building block for polyethylene plastics (C2H4)',
        'simple_ar': 'اللبنة الأساسية لبلاستيك البولي إيثيلين',
        'detailed': 'Ethylene (C2H4) is the simplest alkene and the world\'s most produced organic compound. Produced by steam cracking of hydrocarbons at 750-900°C. Polymer-grade ethylene has purity >99.9% and is the primary feedstock for polyethylene (PE). At ETHYDCO: 460,000 T/Year.'
    },
    'propylene': {
        'term': 'Propylene',
        'term_ar': 'البروبيلين',
        'simple': 'Olefin used for polypropylene and chemicals (C3H6)',
        'simple_ar': 'أوليفين يستخدم في البولي بروبيلين والكيماويات',
        'detailed': 'Propylene (C3H6) is the second most important olefin. It\'s a byproduct of steam cracking, recovered in the C3s stream. At ETHYDCO, the C3s stream contains 69.5-74 mol% propylene and is used as fuel or exported.'
    },
    'butadiene': {
        'term': '1,3-Butadiene',
        'term_ar': 'البيوتادايين',
        'simple': 'Diene used for synthetic rubber production (C4H6)',
        'simple_ar': 'ثنائي الإيثيلين يستخدم في إنتاج المطاط الصناعي',
        'detailed': '1,3-Butadiene is a conjugated diene extracted from the C4 stream of steam crackers. Used for synthetic rubber (SBR, polybutadiene, NBR). ETHYDCO produces 20,000 T/Year using extractive distillation.'
    },
    'pyrolysis_gasoline': {
        'term': 'Pyrolysis Gasoline',
        'term_ar': 'بنزين التكسير',
        'simple': 'Liquid byproduct from cracking, rich in aromatics',
        'simple_ar': 'منتج سائل من التكسير غني بالعطريات',
        'detailed': 'Pyrolysis gasoline (PyGas) is condensed from cracker effluent. Rich in aromatics (BTX), styrene, and heavy components. At ETHYDCO: 70-250 Kg/hr from quench tower, used as fuel.'
    },
    'h2_offgas': {
        'term': 'H2 Offgas',
        'term_ar': 'غاز الهيدروجين',
        'simple': 'Hydrogen-rich stream from cold box separation',
        'simple_ar': 'تيار غني بالهيدروجين من الفصل المبرد',
        'detailed': 'H2 offgas is recovered from the cold box cryogenic unit. At ETHYDCO: 87-90 mol% H2 with CH4 and CO. Design: 6.812 T/hr, Actual: 4-4.5 T/hr. Used as fuel in cracker furnaces.'
    },
    'methane_offgas': {
        'term': 'Methane Offgas',
        'term_ar': 'غاز الميثان',
        'simple': 'Methane-rich stream from demethanizer column',
        'simple_ar': 'تيار غني بالميثان من عمود إزالة الميثان',
        'detailed': 'Methane offgas is the overhead from the demethanizer column. At ETHYDCO: 76-82.5 mol% CH4, 17-22 mol% H2. Design: 4.5-6.2 T/hr, Actual: 3-4.5 T/hr. Used as fuel gas.'
    },
    'lpg': {
        'term': 'LPG',
        'term_ar': 'غاز البترول المسال',
        'simple': 'Liquefied Petroleum Gas - propane and butane mixture',
        'simple_ar': 'خليط البروبان والبيوتان',
        'detailed': 'LPG consists of propane (C3) and butane (C4). At ETHYDCO, C3s and C4s streams are byproducts that can be marketed as LPG or used as fuel. C4s: 0.7 T/hr actual.'
    },
    'cracker': {
        'term': 'Steam Cracker',
        'term_ar': 'التكسير البخاري',
        'simple': 'Unit that breaks down hydrocarbons into olefins',
        'simple_ar': 'وحدة تحول الهيدروكربونات إلى أوليفينات',
        'detailed': 'Steam crackers thermally decompose hydrocarbons at 750-900°C with steam. Cracked gas is cooled and separated to recover ethylene, propylene, and other products. ETHYDCO uses ethane/propane feed (95/5 wt%).'
    },
    'cold_box': {
        'term': 'Cold Box',
        'term_ar': 'الصندوق البارد',
        'simple': 'Cryogenic separation unit for light gases',
        'simple_ar': 'وحدة فصل مبردة للغازات الخفيفة',
        'detailed': 'The cold box operates at -100 to -160°C to separate H2 and CH4 from cracked gas. Uses multi-stage heat exchangers and expanders. Produces H2 offgas and feeds the demethanizer.'
    },
    'demethanizer': {
        'term': 'Demethanizer',
        'term_ar': 'عمود إزالة الميثان',
        'simple': 'Column separating methane from heavier hydrocarbons',
        'simple_ar': 'عمود لفصل الميثان عن الهيدروكربونات الثقيلة',
        'detailed': 'The demethanizer is a high-pressure distillation column separating CH4 overhead from C2+ bottoms. Operates at cryogenic temperatures. Overhead is methane offgas; bottoms proceed to deethanizer.'
    },
    'amine_stripper': {
        'term': 'Amine Stripper',
        'term_ar': 'منزع الأمين',
        'simple': 'Regenerator for amine solution by stripping CO2/H2S',
        'simple_ar': 'وحدة تجديد محلول الأمين بإزالة CO2/H2S',
        'detailed': 'The amine stripper regenerates rich amine by heating to release CO2 and H2S. At ETHYDCO: Offgas is 90 mol% CO2 with H2S traces, sent to incinerator. Design: 23.2 T/hr, Actual: 16-18 T/hr.'
    },
    'quench_tower': {
        'term': 'Quench Tower',
        'term_ar': 'برج التبريد السريع',
        'simple': 'Rapid cooling unit for hot cracked gas',
        'simple_ar': 'وحدة تبريد سريع لغاز التكسير الساخن',
        'detailed': 'The quench tower rapidly cools cracker effluent from ~850°C to ~40°C using circulating oil/water. Stops secondary reactions and condenses pyrolysis gasoline. Cooled gas proceeds to compression.'
    }
}


# ============================================================================
# DATA EXTRACTION
# ============================================================================

def load_metrics():
    """Extract key metrics from the Excel file."""
    metrics = {}

    # Product Prices
    metrics['prices'] = {
        'H2': 2000, 'C2H6': 400, 'C2H4': 400, 'LPG': 729,
        'C5+': 620, 'Methanol': 450, 'Ethylene_MTO': 1200, 'Propylene_MTO': 900
    }

    # Streams
    metrics['streams'] = {
        'names': ['Flare Gas OLD', 'Flare Gas New', 'Refinery Gas', 'PSA Purge', 'Sweep Gas', 'Penex'],
        'names_ar': ['غاز الشعلة القديم', 'غاز الشعلة الجديد', 'غاز المصفاة', 'تنظيف PSA', 'غاز الكنس', 'بنيكس'],
        'flow_kgh': [4122, 2989, 48459.44, 62786.45, 3723.42, 2088.12],
        'flow_ty': [32976, 23912, 387675.54, 502291.59, 29787.34, 16704.93],
    }

    # Products
    metrics['products'] = {
        'H2': 39444.77, 'CH4': 251737.80, 'C2H6': 59230.02, 'C2H4': 2062.40,
        'C3H8': 57097.95, 'C3H6': 2915.37, 'iC4': 32898.08, 'nC4': 43014.61,
        'C4=': 4631.79, 'C5+': 21733.10, 'CO': 65956.12, 'CO2': 408747.17
    }

    # Stream components
    metrics['stream_components'] = {
        'H2': [4031.75, 3420.66, 16074.74, 10645.69, 2766.34, 2505.59],
        'CH4': [8659.03, 5530.73, 194089.88, 39689.32, 2692.79, 1076.05],
        'C2': [3640.52, 1992.00, 45949.35, 27.45, 7396.02, 2287.08],
        'C3': [4389.92, 3206.61, 36257.20, 48.31, 9011.38, 7099.90],
        'C4': [5636.10, 4645.15, 60600.94, 56.60, 6288.14, 3317.54],
        'C5+': [4396.36, 2768.20, 10851.65, 0, 1397.49, 2319.40],
        'CO': [5313.69, 4069.12, 29206.57, 24952.88, 0, 2413.85],
        'CO2': [2499.26, 2279.22, 0, 401936.87, 135.20, 1896.61]
    }

    # Calculation results
    metrics['calc1'] = {
        'total_LPG': 125508.57, 'total_C5+': 21733.10,
        'LPG_value': 91495749.75, 'C5+_value': 13474523.07,
        'net_value': 76231321.92
    }

    metrics['calc2'] = {
        'total_H2': 39444.77, 'H2_value': 78889537.01,
        'net_value': 61561956.72,
        'H2_sources': {'Off-Gas': 16074.74, 'Flare OLD': 4031.75, 'Flare New': 3420.66,
                       'PSA Purge': 10645.69, 'Sweep Gas': 2766.34, 'Penex': 2505.59}
    }

    metrics['calc3'] = {
        'MIDOR_C2_supply': 59005.34, 'ETHYDCO_C2_need_min': 83600,
        'ETHYDCO_C2_need_max': 121600, 'coverage_min': 0.7058,
        'coverage_max': 0.4852, 'C2_value': 23602135.55
    }

    metrics['calc5'] = {
        'H2_required': 65665.68, 'H2_available': 39444.77,
        'H2_deficit': 26220.91, 'H2_utilization': 0.6007,
        'total_methanol': 224069.87
    }

    metrics['calc6'] = {
        'methanol_in_gasoline': 79539.50, 'methanol_for_MTO': 144530.37,
        'ethylene_from_MTO': 40468.50, 'propylene_from_MTO': 60702.75,
        'methanol_value': 35792775.30, 'ethylene_value': 16187401.19,
        'propylene_value': 44252308.01, 'phase34_net': 96232484.50
    }

    metrics['summary'] = {
        'phase12_gross': 176064779.38, 'phase12_NG_cost': 76231321.92,
        'phase12_net': 99833457.46, 'phase34_net': 96232484.50,
        'total_net': 196065941.97
    }

    return metrics

# ============================================================================
# CHART GENERATORS - Optimized for readability
# ============================================================================

def create_phase_donut(metrics, lang='en'):
    """Create donut chart for phase distribution."""
    if lang == 'ar':
        labels = ['المرحلة 1+2: استرداد الغاز', 'المرحلة 3+4: الميثانول']
        title = 'توزيع القيمة حسب المرحلة'
    else:
        labels = ['Phase 1+2: Gas Recovery', 'Phase 3+4: Methanol & MTO']
        title = 'Value Distribution by Phase'

    values = [metrics['summary']['phase12_net'], metrics['summary']['phase34_net']]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=['#06b6d4', '#f59e0b'], line=dict(color='white', width=3)),
        textinfo='percent',
        textfont=dict(size=16, color='white', family='Inter'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        direction='clockwise',
        sort=False
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5,
                   font=dict(size=12, family='Inter', color='#f1f5f9')),
        annotations=[dict(text=f'<b>${sum(values)/1e6:.0f}M</b>', x=0.5, y=0.5,
                         font=dict(size=28, family='Inter', color='#f1f5f9'), showarrow=False)],
        margin=dict(t=20, b=70, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320,
        autosize=True
    )

    return fig

def create_product_bars(metrics, lang='en'):
    """Create horizontal bar chart for product values."""
    if lang == 'ar':
        products = ['غاز مسال (LPG)', 'نافثا (C5+)', 'هيدروجين (H2)', 'إيثان (C2)',
                   'ميثانول', 'إيثيلين MTO', 'بروبيلين MTO']
        title = 'قيم المنتجات السنوية'
        xaxis_title = 'القيمة (مليون دولار/سنة)'
    else:
        products = ['LPG (C3+C4)', 'Naphtha (C5+)', 'Hydrogen (H2)', 'Ethane (C2)',
                   'Methanol Blend', 'Ethylene (MTO)', 'Propylene (MTO)']
        title = 'Annual Product Values'
        xaxis_title = 'Value ($ Million/year)'

    values = [
        metrics['calc1']['LPG_value'] / 1e6,
        metrics['calc1']['C5+_value'] / 1e6,
        metrics['calc2']['H2_value'] / 1e6,
        metrics['calc3']['C2_value'] / 1e6,
        metrics['calc6']['methanol_value'] / 1e6,
        metrics['calc6']['ethylene_value'] / 1e6,
        metrics['calc6']['propylene_value'] / 1e6
    ]

    colors = ['#06b6d4', '#06b6d4', '#0ea5e9', '#0ea5e9', '#f59e0b', '#f59e0b', '#f59e0b']

    fig = go.Figure(data=[
        go.Bar(
            y=products,
            x=values,
            orientation='h',
            marker=dict(color=colors, line=dict(width=0)),
            text=[f'${v:.1f}M' for v in values],
            textposition='outside',
            textfont=dict(size=13, family='Inter', color='#f1f5f9'),
            hovertemplate='<b>%{y}</b><br>$%{x:.1f}M<extra></extra>'
        )
    ])

    fig.update_layout(
        xaxis=dict(title=dict(text=xaxis_title, font=dict(size=12, color='#f1f5f9')),
                   tickfont=dict(size=11, color='#f1f5f9'),
                   gridcolor='rgba(255,255,255,0.1)', showgrid=True, range=[0, max(values)*1.35]),
        yaxis=dict(tickfont=dict(size=11, family='Inter', color='#f1f5f9'), autorange='reversed'),
        margin=dict(t=30, b=60, l=120, r=70),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        bargap=0.35,
        autosize=True
    )

    return fig

def create_cost_benefit_bars(metrics, lang='en'):
    """Create grouped bar chart for cost-benefit analysis."""
    if lang == 'ar':
        categories = ['المرحلة 1+2', 'المرحلة 3+4']
        legend_labels = ['القيمة الإجمالية', 'تكلفة الغاز الطبيعي', 'القيمة الصافية']
        title = 'تحليل التكلفة والعائد'
    else:
        categories = ['Phase 1+2', 'Phase 3+4']
        legend_labels = ['Gross Value', 'NG Makeup Cost', 'Net Value']
        title = 'Cost-Benefit Analysis'

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name=legend_labels[0],
        x=categories,
        y=[metrics['summary']['phase12_gross']/1e6, metrics['calc6']['phase34_net']/1e6],
        marker_color='#22c55e',
        text=[f"${metrics['summary']['phase12_gross']/1e6:.0f}M", f"${metrics['calc6']['phase34_net']/1e6:.0f}M"],
        textposition='outside',
        textfont=dict(size=12, color='#f1f5f9')
    ))

    fig.add_trace(go.Bar(
        name=legend_labels[1],
        x=categories,
        y=[metrics['summary']['phase12_NG_cost']/1e6, 0],
        marker_color='#ef4444',
        text=[f"${metrics['summary']['phase12_NG_cost']/1e6:.0f}M", "$0M"],
        textposition='outside',
        textfont=dict(size=12, color='#f1f5f9')
    ))

    fig.add_trace(go.Bar(
        name=legend_labels[2],
        x=categories,
        y=[metrics['summary']['phase12_net']/1e6, metrics['summary']['phase34_net']/1e6],
        marker_color='#0ea5e9',
        text=[f"${metrics['summary']['phase12_net']/1e6:.0f}M", f"${metrics['summary']['phase34_net']/1e6:.0f}M"],
        textposition='outside',
        textfont=dict(size=12, color='#f1f5f9')
    ))

    yaxis_title = 'القيمة (مليون $)' if lang == 'ar' else 'Value ($ Million)'

    fig.update_layout(
        barmode='group',
        legend=dict(orientation='h', yanchor='bottom', y=1.08, xanchor='center', x=0.5,
                   font=dict(size=11, color='#f1f5f9')),
        xaxis=dict(tickfont=dict(size=12, family='Inter', color='#f1f5f9')),
        yaxis=dict(title=dict(text=yaxis_title, font=dict(size=11, color='#f1f5f9')),
                   tickfont=dict(size=10, color='#f1f5f9'), gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(t=80, b=40, l=60, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        bargap=0.25,
        autosize=True
    )

    return fig

def create_sankey(metrics, lang='en'):
    """Create Sankey diagram for material/value flow."""
    if lang == 'ar':
        labels = ['غاز الشعلة', 'غاز المصفاة', 'PSA + كنس', 'بنيكس',
                 'استرداد H2', 'استرداد LPG', 'استرداد C5+', 'استرداد C2',
                 'CO/CO2', 'ميثانول', 'منتجات MTO', 'القيمة الصافية']
    else:
        labels = ['Flare Gas', 'Refinery Gas', 'PSA + Sweep', 'Penex',
                 'H2 Recovery', 'LPG Recovery', 'C5+ Recovery', 'C2 Recovery',
                 'CO/CO2', 'Methanol', 'MTO Products', 'Net Value']

    # Source -> Target connections
    source = [0,0,0, 1,1,1,1, 2,2,2, 3,3,3, 4, 5, 6, 7, 8, 9, 10]
    target = [4,5,6, 4,5,6,7, 4,5,8, 4,5,6, 11, 11, 11, 11, 9, 10, 11]
    value =  [7.5,7.6,7.2, 16,36,11,46, 13,9,25, 2.5,7,2.3, 79, 91, 13, 24, 224, 101, 60]

    node_colors = ['#f97316', '#f97316', '#f97316', '#f97316',
                   '#0ea5e9', '#06b6d4', '#06b6d4', '#0ea5e9',
                   '#8b5cf6', '#f59e0b', '#f59e0b', '#22c55e']

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color='white', width=2),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(100,100,100,0.15)'
        )
    )])

    fig.update_layout(
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        font=dict(size=12, family='Inter', color='#f1f5f9'),
        autosize=True
    )

    return fig

def create_gauge(value, max_val, title, lang='en'):
    """Create a modern gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value * 100,
        number={'suffix': '%', 'font': {'size': 36, 'family': 'Inter', 'color': '#f1f5f9'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': '#f1f5f9',
                    'tickfont': {'size': 10, 'color': '#f1f5f9'}},
            'bar': {'color': '#06b6d4', 'thickness': 0.8},
            'bgcolor': 'rgba(0,0,0,0.05)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239,68,68,0.2)'},
                {'range': [50, 75], 'color': 'rgba(245,158,11,0.2)'},
                {'range': [75, 100], 'color': 'rgba(34,197,94,0.2)'}
            ],
        }
    ))

    fig.update_layout(
        margin=dict(t=20, b=10, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        height=200,
        font=dict(family='Inter', color='#f1f5f9'),
        autosize=True
    )

    return fig

def create_h2_balance(metrics, lang='en'):
    """Create H2 balance visualization."""
    if lang == 'ar':
        categories = ['H2 المتوفر', 'H2 المطلوب', 'العجز']
        title = 'توازن الهيدروجين لإنتاج الميثانول'
    else:
        categories = ['H2 Available', 'H2 Required', 'Deficit']
        title = 'H2 Balance for Methanol'

    values = [metrics['calc5']['H2_available']/1000,
              metrics['calc5']['H2_required']/1000,
              metrics['calc5']['H2_deficit']/1000]
    colors = ['#22c55e', '#0ea5e9', '#ef4444']

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f'{v:.1f}K' for v in values],
            textposition='outside',
            textfont=dict(size=14, family='Inter', color='#f1f5f9'),
            width=0.6
        )
    ])

    utilization = metrics['calc5']['H2_utilization'] * 100
    fig.add_annotation(
        x=1, y=max(values)*1.1,
        text=f"<b>Utilization: {utilization:.0f}%</b>" if lang == 'en' else f"<b>نسبة الاستخدام: {utilization:.0f}%</b>",
        showarrow=False,
        font=dict(size=14, color='#0ea5e9', family='Inter')
    )

    fig.update_layout(
        yaxis=dict(title=dict(text='Quantity (kt/year)' if lang == 'en' else 'الكمية (ألف طن/سنة)', font=dict(size=10, color='#f1f5f9')),
                   gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=10, color='#f1f5f9')),
        xaxis=dict(tickfont=dict(size=10, family='Inter', color='#f1f5f9')),
        margin=dict(t=40, b=30, l=50, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        autosize=True
    )

    return fig

def create_stream_heatmap(metrics, lang='en'):
    """Create component distribution heatmap."""
    if lang == 'ar':
        streams = ['شعلة قديم', 'شعلة جديد', 'مصفاة', 'PSA', 'كنس', 'بنيكس']
    else:
        streams = ['Flare OLD', 'Flare New', 'Refinery', 'PSA', 'Sweep', 'Penex']

    components = ['H2', 'CH4', 'C2', 'C3', 'C4', 'C5+', 'CO', 'CO2']

    z = []
    for comp in components:
        row = metrics['stream_components'][comp]
        total = sum(row)
        if total > 0:
            z.append([v/1000 for v in row])  # Convert to thousands
        else:
            z.append([0]*6)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=streams,
        y=components,
        colorscale='Viridis',
        text=[[f'{v:.0f}' if v > 0 else '' for v in row] for row in z],
        texttemplate='%{text}',
        textfont={"size": 10, "color": "white"},
        hovertemplate='%{y} in %{x}: %{z:.1f}K t/y<extra></extra>',
        colorbar=dict(title=dict(text='kt/y', font=dict(size=11, color='#f1f5f9')), tickfont=dict(size=10, color='#f1f5f9'))
    ))

    fig.update_layout(
        xaxis=dict(tickfont=dict(size=10, family='Inter', color='#f1f5f9'), side='bottom',
                   tickangle=-45),
        yaxis=dict(tickfont=dict(size=10, family='Inter', color='#f1f5f9'), autorange='reversed'),
        margin=dict(t=20, b=60, l=50, r=80),
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        autosize=True
    )

    return fig

def create_methanol_allocation(metrics, lang='en'):
    """Create methanol allocation pie."""
    if lang == 'ar':
        labels = ['مزج البنزين', 'تحويل MTO']
    else:
        labels = ['Gasoline Blending', 'MTO Conversion']

    values = [metrics['calc6']['methanol_in_gasoline'], metrics['calc6']['methanol_for_MTO']]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=['#06b6d4', '#f59e0b'], line=dict(color='white', width=2)),
        textinfo='percent+label',
        textposition='outside',
        textfont=dict(size=12, family='Inter', color='#f1f5f9'),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} t/y<br>%{percent}<extra></extra>'
    )])

    fig.update_layout(
        showlegend=False,
        margin=dict(t=30, b=30, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        autosize=True
    )

    return fig


# ============================================================================
# ETHYDCO KNOWLEDGE BASE CHARTS
# ============================================================================

def get_numeric_value(val):
    """Extract numeric value from design/actual value (handles ranges)."""
    if val is None:
        return None
    if isinstance(val, dict) and 'min' in val:
        return (val['min'] + val['max']) / 2
    if isinstance(val, (int, float)):
        return val
    return None

def create_design_actual_chart(ethydco_data, lang='en'):
    """Create grouped bar chart comparing design vs actual capacity."""
    items = []
    design_vals = []
    actual_vals = []

    # Collect all items with both design and actual values
    all_items = (ethydco_data['feeds'] + ethydco_data['products'] +
                 ethydco_data['fuel_gas'] + ethydco_data['other_gases'])

    for item in all_items:
        design = get_numeric_value(item.get('design_value'))
        actual = get_numeric_value(item.get('actual_value'))

        if design is not None and actual is not None:
            name = item.get('name_ar' if lang == 'ar' else 'name', item['name'])
            # Truncate long names
            if len(name) > 25:
                name = name[:22] + '...'
            items.append(name)

            # Normalize units to T/hr for comparison
            design_unit = item.get('design_unit', '')
            actual_unit = item.get('actual_unit', design_unit)

            # Convert Kg/hr to T/hr
            if 'Kg' in design_unit:
                design = design / 1000
            if 'Kg' in actual_unit:
                actual = actual / 1000
            # Convert T/Year to T/hr
            if 'Year' in design_unit:
                design = design / OPERATING_HOURS_PER_YEAR
            if 'Year' in actual_unit:
                actual = actual / OPERATING_HOURS_PER_YEAR

            design_vals.append(design)
            actual_vals.append(actual)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Design' if lang == 'en' else 'التصميم',
        x=items,
        y=design_vals,
        marker_color='#0ea5e9',
        text=[f'{v:.1f}' for v in design_vals],
        textposition='outside',
        textfont=dict(size=10, color='#f1f5f9')
    ))

    fig.add_trace(go.Bar(
        name='Actual' if lang == 'en' else 'الفعلي',
        x=items,
        y=actual_vals,
        marker_color='#22c55e',
        text=[f'{v:.1f}' for v in actual_vals],
        textposition='outside',
        textfont=dict(size=10, color='#f1f5f9')
    ))

    fig.update_layout(
        barmode='group',
        xaxis=dict(tickangle=-45, tickfont=dict(size=9, color='#f1f5f9')),
        yaxis=dict(
            title=dict(text='T/hr' if lang == 'en' else 'طن/ساعة', font=dict(size=10, color='#f1f5f9')),
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=10, color='#f1f5f9')
        ),
        legend=dict(orientation='h', y=1.15, xanchor='center', x=0.5, font=dict(size=11, color='#f1f5f9')),
        margin=dict(t=60, b=120, l=60, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        bargap=0.2
    )

    return fig


def create_routing_sankey(ethydco_data, lang='en'):
    """Create Sankey diagram showing stream routing at ETHYDCO."""

    if lang == 'ar':
        nodes = [
            'خط جاسكو',           # 0
            'التنقية',            # 1
            'التكسير البخاري',    # 2
            'الصندوق البارد',     # 3
            'عمود الميثان',       # 4
            'عمود C3',           # 5
            'عمود C4',           # 6
            'برج التبريد',        # 7
            'منزع الأمين',        # 8
            'مصنع PE',           # 9
            'وحدة البيوتادايين',  # 10
            'نظام الوقود',        # 11
            'المحرقة',            # 12
            'التصدير'             # 13
        ]
    else:
        nodes = [
            'GASCO Pipeline',      # 0
            'Purification',        # 1
            'Steam Crackers',      # 2
            'Cold Box',            # 3
            'Demethanizer',        # 4
            'De-C3 Column',        # 5
            'De-C4 Column',        # 6
            'Quench Tower',        # 7
            'Amine Stripper',      # 8
            'PE Plant',            # 9
            'Butadiene Unit',      # 10
            'Fuel Gas System',     # 11
            'Incinerator',         # 12
            'Export'               # 13
        ]

    # Define links (source, target, value in T/hr equivalent)
    links = [
        (0, 1, 70),    # GASCO -> Purification (Feed)
        (1, 2, 70),    # Purification -> Crackers
        (2, 3, 30),    # Crackers -> Cold Box
        (2, 4, 25),    # Crackers -> Demethanizer
        (2, 7, 5),     # Crackers -> Quench Tower
        (3, 11, 4.5),  # Cold Box -> Fuel (H2 offgas)
        (3, 4, 20),    # Cold Box -> Demethanizer
        (4, 11, 4),    # Demethanizer -> Fuel (CH4 offgas)
        (4, 5, 15),    # Demethanizer -> De-C3
        (5, 11, 2.5),  # De-C3 -> Fuel (C3s)
        (5, 6, 10),    # De-C3 -> De-C4
        (6, 10, 5),    # De-C4 -> Butadiene Unit
        (6, 13, 0.7),  # De-C4 -> Export (C4s)
        (10, 13, 2.5), # Butadiene -> Export
        (3, 9, 57.5),  # Cold Box -> PE Plant (Ethylene)
        (7, 11, 0.2),  # Quench Tower -> Fuel (PyGas)
        (8, 12, 17),   # Amine Stripper -> Incinerator
        (0, 11, 1),    # GASCO -> Fuel (NG import)
    ]

    source = [l[0] for l in links]
    target = [l[1] for l in links]
    value = [l[2] for l in links]

    node_colors = [
        '#f59e0b',  # GASCO - orange
        '#8b5cf6',  # Purification - purple
        '#ef4444',  # Crackers - red
        '#0ea5e9',  # Cold Box - blue
        '#0ea5e9',  # Demethanizer - blue
        '#06b6d4',  # De-C3 - cyan
        '#06b6d4',  # De-C4 - cyan
        '#f97316',  # Quench - orange
        '#64748b',  # Amine Stripper - gray
        '#22c55e',  # PE Plant - green
        '#8b5cf6',  # Butadiene - purple
        '#22c55e',  # Fuel Gas - green
        '#64748b',  # Incinerator - gray
        '#22c55e',  # Export - green
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color='white', width=1),
            label=nodes,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(100,100,100,0.2)'
        )
    )])

    fig.update_layout(
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        height=420,
        font=dict(size=11, family='Inter', color='#f1f5f9')
    )

    return fig


# ============================================================================
# HTML GENERATION - KNOWLEDGE BASE
# ============================================================================

def format_value_display(value, unit=''):
    """Format a value for display (handles ranges and None)."""
    if value is None:
        return 'N/A'
    if isinstance(value, dict) and 'min' in value:
        return f"{value['min']} - {value['max']}"
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        if value >= 1000:
            return f"{value:,.0f}"
        return f"{value:.2f}"
    return str(value)

def format_composition_html(composition, comp_unit):
    """Format composition data as HTML list."""
    if not composition:
        return ''

    lines = []
    for key, val in composition.items():
        if isinstance(val, dict) and 'min' in val:
            lines.append(f"<li><span class='comp-name'>{key}:</span> <span class='comp-val'>{val['min']}-{val['max']} {comp_unit}</span></li>")
        else:
            lines.append(f"<li><span class='comp-name'>{key}:</span> <span class='comp-val'>{val} {comp_unit}</span></li>")

    return '<ul class="comp-list">' + ''.join(lines) + '</ul>'

def generate_kb_cards(ethydco_data):
    """Generate Knowledge Base expandable cards HTML."""
    cards = []

    # Combine all items
    all_items = []
    for item in ethydco_data['feeds']:
        all_items.append(item)
    for item in ethydco_data['products']:
        all_items.append(item)
    for item in ethydco_data['flared_gases']:
        all_items.append(item)
    for item in ethydco_data['fuel_gas']:
        all_items.append(item)
    for item in ethydco_data['other_gases']:
        all_items.append(item)

    for item in all_items:
        item_id = item['id']
        name = item['name']
        name_ar = item.get('name_ar', name)
        category = item['category']
        data_source = item.get('data_source', '')

        # Get design/actual values
        design_val = item.get('design_value')
        design_unit = item.get('design_unit', '')
        actual_val = item.get('actual_value')
        actual_unit = item.get('actual_unit', design_unit)

        # Format display values
        design_display = format_value_display(design_val)
        actual_display = format_value_display(actual_val)

        # Calculate utilization percentage for progress bar
        design_num = get_numeric_value(design_val)
        actual_num = get_numeric_value(actual_val)
        if design_num and actual_num and design_num > 0:
            utilization_pct = min(100, (actual_num / design_num) * 100)
        else:
            utilization_pct = 0

        # Get composition
        composition = item.get('composition', {})
        comp_unit = item.get('composition_unit', '')
        composition_html = format_composition_html(composition, comp_unit)

        # Get conditions
        conditions = item.get('conditions', {})
        conditions_html = ''
        if conditions:
            cond_items = []
            if 'P' in conditions:
                p_unit = conditions.get('P_unit', 'kg/cm²g')
                cond_items.append(f"<div class='condition-item'><span class='cond-label'>P</span><span class='cond-value'>{conditions['P']} {p_unit}</span></div>")
            if 'T' in conditions:
                t_unit = conditions.get('T_unit', '°C')
                cond_items.append(f"<div class='condition-item'><span class='cond-label'>T</span><span class='cond-value'>{conditions['T']} {t_unit}</span></div>")
            if 'pressure' in conditions:
                p_data = conditions['pressure']
                if isinstance(p_data, dict):
                    cond_items.append(f"<div class='condition-item'><span class='cond-label'>P (min)</span><span class='cond-value'>{p_data['min']} {p_data.get('unit', '')}</span></div>")
            if 'temperature' in conditions:
                cond_items.append(f"<div class='condition-item'><span class='cond-label'>T</span><span class='cond-value'>{conditions['temperature']}</span></div>")
            if 'phase' in conditions:
                cond_items.append(f"<div class='condition-item'><span class='cond-label'>Phase</span><span class='cond-value'>{conditions['phase']}</span></div>")
            conditions_html = ''.join(cond_items)

        # Get routing
        routing = item.get('routing', {})
        routing_html = ''
        if routing:
            source = routing.get('source', '')
            source_ar = routing.get('source_ar', source)
            dest = routing.get('destination', '')
            dest_ar = routing.get('destination_ar', dest)
            routing_html = f'''
            <div class="routing-section">
                <h4 class="en-only">Stream Routing</h4>
                <h4 class="ar-only">مسار التيار</h4>
                <div class="routing-flow">
                    <div class="route-node source">
                        <span class="en-only">{source}</span>
                        <span class="ar-only">{source_ar}</span>
                    </div>
                    <div class="route-arrow">→</div>
                    <div class="route-node destination">
                        <span class="en-only">{dest}</span>
                        <span class="ar-only">{dest_ar}</span>
                    </div>
                </div>
            </div>
            '''

        # Get comments
        comment = item.get('comment', '')
        comment_ar = item.get('comment_ar', comment)
        comment_html = ''
        if comment:
            comment_html = f'''
            <div class="comments-section">
                <h4 class="en-only">Notes</h4>
                <h4 class="ar-only">ملاحظات</h4>
                <p class="en-only">{comment}</p>
                <p class="ar-only">{comment_ar}</p>
            </div>
            '''

        # Get definition
        def_key = item.get('definition_key', '')
        definition_html = ''
        if def_key and def_key in DEFINITIONS:
            defn = DEFINITIONS[def_key]
            definition_html = f'''
            <div class="definition-toggle" onclick="toggleDefinition(this)">
                <span class="en-only">📖 What is {defn['term']}?</span>
                <span class="ar-only">📖 ما هو {defn['term_ar']}؟</span>
                <span class="toggle-icon">+</span>
            </div>
            <div class="definition-content">
                <p class="simple-def en-only">{defn['simple']}</p>
                <p class="simple-def ar-only">{defn['simple_ar']}</p>
                <div class="detailed-def">
                    <p>{defn['detailed']}</p>
                </div>
            </div>
            '''

        # Handle special items (impurities, limitations, flares)
        special_content = ''
        if 'fresh_feed' in item:
            fresh = item['fresh_feed']
            treated = item['treated_feed']
            special_content = f'''
            <div class="special-section">
                <h4 class="en-only">Fresh Feed (from GASCO)</h4>
                <h4 class="ar-only">التغذية الطازجة (من جاسكو)</h4>
                <ul class="comp-list">
                    <li>CO2: {fresh['CO2']['value']} {fresh['CO2']['unit']}</li>
                    <li>H2S: {fresh['H2S']['value']} {fresh['H2S']['unit']}</li>
                    <li>Hg: {fresh['Hg']['value']} {fresh['Hg']['unit']}</li>
                </ul>
                <h4 class="en-only" style="margin-top:15px;">Treated Feed (to Crackers)</h4>
                <h4 class="ar-only" style="margin-top:15px;">التغذية المعالجة (للتكسير)</h4>
                <ul class="comp-list">
                    <li>CO2: {treated['CO2']['value']} {treated['CO2']['unit']}</li>
                    <li>H2S: {treated['H2S']}</li>
                    <li>Hg: {treated['Hg']}</li>
                </ul>
            </div>
            '''

        if 'limitations' in item:
            lims = item['limitations']
            lims_ar = item.get('limitations_ar', lims)
            lim_items_en = ''.join([f'<li>{l}</li>' for l in lims])
            lim_items_ar = ''.join([f'<li>{l}</li>' for l in lims_ar])
            special_content = f'''
            <div class="special-section">
                <h4 class="en-only">Feed Limitations</h4>
                <h4 class="ar-only">قيود التغذية</h4>
                <ul class="comp-list en-only">{lim_items_en}</ul>
                <ul class="comp-list ar-only">{lim_items_ar}</ul>
            </div>
            '''

        if 'flare_type' in item:
            special_content = f'''
            <div class="special-section">
                <div class="data-row">
                    <span class="en-only">Flare Type:</span>
                    <span class="ar-only">نوع الشعلة:</span>
                    <span class="en-only">{item['flare_type']}</span>
                    <span class="ar-only">{item.get('flare_type_ar', item['flare_type'])}</span>
                </div>
                <div class="data-row">
                    <span class="en-only">Operation:</span>
                    <span class="ar-only">التشغيل:</span>
                    <span class="en-only">{item['flow']}</span>
                    <span class="ar-only">{item.get('flow_ar', item['flow'])}</span>
                </div>
                <div class="data-row">
                    <span class="en-only">Measured:</span>
                    <span class="ar-only">مقاس:</span>
                    <span>{'No' if not item.get('is_measured', False) else 'Yes'}</span>
                </div>
            </div>
            '''

        if 'description' in item:
            special_content = f'''
            <div class="special-section">
                <p class="en-only">{item['description']}</p>
                <p class="ar-only">{item.get('description_ar', item['description'])}</p>
            </div>
            '''

        # Generate card icon based on category
        icon_map = {
            'feeds': '⚡',
            'products': '📦',
            'flares': '🔥',
            'fuel': '⛽',
            'other': '🌀'
        }
        icon = icon_map.get(category, '📋')

        # Build capacity section if values exist
        capacity_section = ''
        if design_val is not None or actual_val is not None:
            capacity_section = f'''
            <div class="capacity-section">
                <div class="capacity-row">
                    <span class="label en-only">Design Capacity:</span>
                    <span class="label ar-only">السعة التصميمية:</span>
                    <span class="value design" data-value="{get_numeric_value(design_val) or ''}" data-unit="{design_unit}">{design_display} {design_unit}</span>
                </div>
                <div class="capacity-row">
                    <span class="label en-only">Actual Capacity:</span>
                    <span class="label ar-only">السعة الفعلية:</span>
                    <span class="value actual" data-value="{get_numeric_value(actual_val) or ''}" data-unit="{actual_unit}">{actual_display} {actual_unit}</span>
                </div>
                <div class="capacity-bar">
                    <div class="bar-fill" style="width: {utilization_pct:.0f}%"></div>
                </div>
                <div class="utilization-label" style="text-align:right; font-size:0.8rem; color:#64748b; margin-top:5px;">
                    {utilization_pct:.0f}% <span class="en-only">utilization</span><span class="ar-only">استخدام</span>
                </div>
            </div>
            '''

        # Build composition section
        comp_section = ''
        if composition_html:
            comp_section = f'''
            <div class="composition-section">
                <h4 class="en-only">Composition ({comp_unit})</h4>
                <h4 class="ar-only">التركيب ({comp_unit})</h4>
                {composition_html}
                <div class="comp-chart" id="comp-{item_id}"></div>
            </div>
            '''

        # Build conditions section
        cond_section = ''
        if conditions_html:
            cond_section = f'''
            <div class="conditions-section">
                <h4 class="en-only">Operating Conditions</h4>
                <h4 class="ar-only">ظروف التشغيل</h4>
                <div class="conditions-grid">
                    {conditions_html}
                </div>
            </div>
            '''

        # Build complete card
        card = f'''
        <div class="kb-card" data-category="{category}" data-id="{item_id}"
             data-design-value="{get_numeric_value(design_val) or ''}"
             data-design-unit="{design_unit}"
             data-actual-value="{get_numeric_value(actual_val) or ''}"
             data-actual-unit="{actual_unit}">
            <div class="kb-card-header" onclick="toggleCard(this)">
                <div class="kb-card-icon">{icon}</div>
                <div class="kb-card-title">
                    <h3 class="en-only">{name}</h3>
                    <h3 class="ar-only">{name_ar}</h3>
                    <span class="kb-card-subtitle">{category.title()} | {data_source}</span>
                </div>
                <div class="kb-card-summary">
                    <div class="summary-value">
                        <span class="design-value">{design_display if design_val else ''}</span>
                        <span class="actual-value">{actual_display if actual_val else ''}</span>
                        <span class="unit">{design_unit}</span>
                    </div>
                </div>
                <div class="kb-card-expand">
                    <span class="expand-icon">▼</span>
                </div>
            </div>
            <div class="kb-card-body">
                {capacity_section}
                {special_content}
                {comp_section}
                {cond_section}
                {routing_html}
                {definition_html}
                {comment_html}
            </div>
        </div>
        '''
        cards.append(card)

    return ''.join(cards)


def generate_definitions_html():
    """Generate definitions/glossary section HTML."""
    cards = []
    for key, defn in DEFINITIONS.items():
        card = f'''
        <div class="def-card" onclick="toggleDefCard(this)">
            <div class="def-term en-only">{defn['term']}</div>
            <div class="def-term ar-only">{defn['term_ar']}</div>
            <div class="def-simple en-only">{defn['simple']}</div>
            <div class="def-simple ar-only">{defn['simple_ar']}</div>
            <div class="def-detailed" style="display:none;">
                <p>{defn['detailed']}</p>
            </div>
        </div>
        '''
        cards.append(card)
    return ''.join(cards)


# ============================================================================
# HTML GENERATION - ORIGINAL DASHBOARD
# ============================================================================

def generate_stream_cards(metrics):
    """Generate stream detail cards HTML."""
    cards = []
    for i in range(6):
        flow_val = metrics['streams']['flow_ty'][i] / 1000
        card = f'''
        <div class="data-card">
            <div class="data-card-header">{metrics['streams']['names'][i]} <span class="ar-only">({metrics['streams']['names_ar'][i]})</span></div>
            <div class="data-card-value">{flow_val:.1f}K <span style="font-size: 0.8rem; color: var(--gray);">t/y</span></div>
            <div class="data-row"><span>H2</span><span>{metrics['stream_components']['H2'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>CH4</span><span>{metrics['stream_components']['CH4'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>C2</span><span>{metrics['stream_components']['C2'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>C3</span><span>{metrics['stream_components']['C3'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>C4</span><span>{metrics['stream_components']['C4'][i]:,.0f} t/y</span></div>
            <div class="data-row"><span>C5+</span><span>{metrics['stream_components']['C5+'][i]:,.0f} t/y</span></div>
        </div>
        '''
        cards.append(card)
    return ''.join(cards)

def generate_prices_table(metrics):
    """Generate product prices table rows."""
    rows = []
    for k, v in metrics['prices'].items():
        rows.append(f'<tr><td>{k}</td><td>${v:,}</td></tr>')
    return ''.join(rows)

def generate_html(metrics):
    """Generate the complete modern HTML dashboard."""

    # Pre-generate stream cards and price table
    stream_cards_html = generate_stream_cards(metrics)
    prices_table_html = generate_prices_table(metrics)

    # Load ETHYDCO data and generate Knowledge Base content
    ethydco_data = load_ethydco_data()
    kb_cards_html = generate_kb_cards(ethydco_data)
    definitions_html = generate_definitions_html()

    # Pre-generate all charts for both languages
    charts = {
        'en': {
            'donut': create_phase_donut(metrics, 'en'),
            'products': create_product_bars(metrics, 'en'),
            'cost_benefit': create_cost_benefit_bars(metrics, 'en'),
            'sankey': create_sankey(metrics, 'en'),
            'gauge_min': create_gauge(metrics['calc3']['coverage_min'], 100, 'Min Coverage', 'en'),
            'gauge_max': create_gauge(metrics['calc3']['coverage_max'], 100, 'Max Coverage', 'en'),
            'h2_balance': create_h2_balance(metrics, 'en'),
            'heatmap': create_stream_heatmap(metrics, 'en'),
            'methanol': create_methanol_allocation(metrics, 'en'),
            'kb_design_actual': create_design_actual_chart(ethydco_data, 'en'),
            'kb_routing': create_routing_sankey(ethydco_data, 'en')
        },
        'ar': {
            'donut': create_phase_donut(metrics, 'ar'),
            'products': create_product_bars(metrics, 'ar'),
            'cost_benefit': create_cost_benefit_bars(metrics, 'ar'),
            'sankey': create_sankey(metrics, 'ar'),
            'gauge_min': create_gauge(metrics['calc3']['coverage_min'], 100, 'تغطية الحد الأدنى', 'ar'),
            'gauge_max': create_gauge(metrics['calc3']['coverage_max'], 100, 'تغطية الحد الأقصى', 'ar'),
            'h2_balance': create_h2_balance(metrics, 'ar'),
            'heatmap': create_stream_heatmap(metrics, 'ar'),
            'methanol': create_methanol_allocation(metrics, 'ar'),
            'kb_design_actual': create_design_actual_chart(ethydco_data, 'ar'),
            'kb_routing': create_routing_sankey(ethydco_data, 'ar')
        }
    }

    # Extract values for KPIs
    total_value = metrics['summary']['total_net']
    phase12 = metrics['summary']['phase12_net']
    phase34 = metrics['summary']['phase34_net']

    # ETHYDCO company info
    company_name = ethydco_data['company_info']['name']
    company_full = ethydco_data['company_info']['full_name']
    company_scope = ethydco_data['company_info']['scope']

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIDOR-ETHYDCO Integration Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        :root {{
            --primary: #0ea5e9;
            --primary-dark: #0284c7;
            --secondary: #06b6d4;
            --accent: #f59e0b;
            --success: #22c55e;
            --danger: #ef4444;
            --dark: #0f172a;
            --dark-light: #1e293b;
            --gray: #64748b;
            --light: #f1f5f9;
            --white: #ffffff;
            --glass: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --shadow-sm: 0 10px 40px -10px rgba(0, 0, 0, 0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, var(--dark) 0%, #1a1a2e 50%, var(--dark-light) 100%);
            min-height: 100vh;
            color: var(--white);
            overflow-x: hidden;
        }}

        body.rtl {{
            direction: rtl;
            font-family: 'Cairo', sans-serif;
        }}

        /* Animated background */
        .bg-animation {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }}

        .bg-animation::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 20% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(245, 158, 11, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(14, 165, 233, 0.1) 0%, transparent 40%);
            animation: rotate 30s linear infinite;
        }}

        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}

        /* Header */
        .header {{
            padding: 30px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(20px);
            background: rgba(15, 23, 42, 0.8);
            border-bottom: 1px solid var(--glass-border);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .logo-icon {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 800;
            box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
        }}

        .logo-text h1 {{
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--white) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .logo-text span {{
            font-size: 0.85rem;
            color: var(--gray);
        }}

        /* Language Toggle */
        .lang-toggle {{
            display: flex;
            background: var(--glass);
            border-radius: 50px;
            padding: 5px;
            border: 1px solid var(--glass-border);
        }}

        .lang-btn {{
            padding: 10px 25px;
            border: none;
            background: transparent;
            color: var(--gray);
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 50px;
            transition: all 0.3s ease;
            font-family: inherit;
        }}

        .lang-btn.active {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: var(--white);
            box-shadow: 0 5px 20px rgba(6, 182, 212, 0.4);
        }}

        .lang-btn:hover:not(.active) {{
            color: var(--white);
        }}

        /* Navigation */
        .nav {{
            display: flex;
            justify-content: center;
            gap: 10px;
            padding: 20px 50px;
            flex-wrap: wrap;
        }}

        .nav-btn {{
            padding: 14px 28px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            color: var(--gray);
            font-size: 0.95rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            font-family: inherit;
        }}

        .nav-btn:hover {{
            background: rgba(14, 165, 233, 0.2);
            border-color: var(--primary);
            color: var(--white);
            transform: translateY(-2px);
        }}

        .nav-btn.active {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-color: transparent;
            color: var(--white);
            box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
        }}

        /* Main Content */
        .content {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 30px 50px 60px;
        }}

        .tab-content {{
            display: none;
            animation: fadeIn 0.5s ease;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* KPI Section */
        .kpi-section {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 25px;
            margin-bottom: 40px;
        }}

        .kpi-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 35px;
            position: relative;
            overflow: hidden;
            transition: all 0.4s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow);
            border-color: var(--primary);
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        }}

        .kpi-card.accent::before {{
            background: linear-gradient(90deg, var(--accent) 0%, #fbbf24 100%);
        }}

        .kpi-card.success::before {{
            background: linear-gradient(90deg, var(--success) 0%, #4ade80 100%);
        }}

        .kpi-card.main {{
            grid-row: span 2;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
        }}

        .kpi-label {{
            font-size: 1rem;
            color: var(--gray);
            margin-bottom: 15px;
            font-weight: 500;
        }}

        .kpi-value {{
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--white) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin-bottom: 15px;
        }}

        .kpi-card.main .kpi-value {{
            font-size: 5.5rem;
        }}

        .kpi-sublabel {{
            font-size: 0.9rem;
            color: var(--gray);
        }}

        .kpi-icon {{
            position: absolute;
            top: 25px;
            right: 25px;
            font-size: 2.5rem;
            opacity: 0.15;
        }}

        .rtl .kpi-icon {{
            right: auto;
            left: 25px;
        }}

        /* Chart Cards */
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
            margin-bottom: 30px;
        }}

        .chart-grid.three {{
            grid-template-columns: repeat(3, 1fr);
        }}

        .chart-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 25px;
            transition: all 0.4s ease;
        }}

        .chart-card:hover {{
            border-color: var(--primary);
            box-shadow: var(--shadow-sm);
        }}

        .chart-card.full {{
            grid-column: 1 / -1;
        }}

        .chart-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--white);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .chart-title::before {{
            content: '';
            width: 4px;
            height: 20px;
            background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 2px;
        }}

        /* Data Cards */
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .data-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
            transition: all 0.3s ease;
        }}

        .data-card:hover {{
            transform: translateY(-3px);
            border-color: var(--secondary);
        }}

        .data-card-header {{
            font-weight: 600;
            font-size: 1rem;
            color: var(--secondary);
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--glass-border);
        }}

        .data-card-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--white);
            margin-bottom: 5px;
        }}

        .data-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px dashed rgba(255,255,255,0.1);
            font-size: 0.9rem;
        }}

        .data-row:last-child {{
            border-bottom: none;
        }}

        .data-row span:first-child {{
            color: var(--gray);
        }}

        .data-row span:last-child {{
            color: var(--white);
            font-weight: 500;
        }}

        /* Gauge Container */
        .gauge-container {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}

        .gauge-card {{
            text-align: center;
        }}

        .gauge-label {{
            font-size: 0.9rem;
            color: var(--gray);
            margin-top: 10px;
        }}

        /* Table Styles */
        .table-container {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
            overflow-x: auto;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .data-table th {{
            background: rgba(14, 165, 233, 0.2);
            color: var(--secondary);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        .rtl .data-table th {{
            text-align: right;
        }}

        .data-table td {{
            padding: 15px;
            border-bottom: 1px solid var(--glass-border);
            color: var(--white);
            font-size: 0.9rem;
        }}

        .data-table tr:hover td {{
            background: rgba(255,255,255,0.05);
        }}

        .data-table .value {{
            color: var(--success);
            font-weight: 600;
        }}

        .data-table .cost {{
            color: var(--danger);
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px;
            color: var(--gray);
            font-size: 0.85rem;
        }}

        /* Responsive */
        @media (max-width: 1200px) {{
            .kpi-section {{
                grid-template-columns: 1fr 1fr;
            }}
            .kpi-card.main {{
                grid-column: 1 / -1;
                grid-row: auto;
            }}
            .chart-grid.three {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 900px) {{
            .header {{
                padding: 20px 25px;
                flex-direction: column;
                gap: 20px;
            }}
            .content {{
                padding: 20px 25px 40px;
            }}
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
            .chart-grid.three {{
                grid-template-columns: 1fr;
            }}
            .kpi-section {{
                grid-template-columns: 1fr;
            }}
            .kpi-card.main .kpi-value {{
                font-size: 3.5rem;
            }}
            .nav {{
                padding: 15px 20px;
            }}
            .nav-btn {{
                padding: 12px 20px;
                font-size: 0.85rem;
            }}
            .gauge-container {{
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }}
            .data-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Mobile phones */
        @media (max-width: 480px) {{
            .header {{
                padding: 15px;
                gap: 15px;
            }}
            .logo-text h1 {{
                font-size: 1.2rem;
            }}
            .logo-text span {{
                font-size: 0.75rem;
            }}
            .logo-icon {{
                width: 40px;
                height: 40px;
                font-size: 20px;
            }}
            .lang-toggle {{
                width: 100%;
                justify-content: center;
            }}
            .lang-btn {{
                padding: 8px 20px;
                font-size: 0.85rem;
            }}
            .nav {{
                padding: 10px 15px;
                gap: 8px;
            }}
            .nav-btn {{
                padding: 10px 14px;
                font-size: 0.8rem;
                border-radius: 10px;
            }}
            .content {{
                padding: 15px 15px 30px;
            }}
            .kpi-card {{
                padding: 20px;
                border-radius: 16px;
            }}
            .kpi-card.main .kpi-value {{
                font-size: 2.8rem;
            }}
            .kpi-value {{
                font-size: 2.5rem;
            }}
            .kpi-label {{
                font-size: 0.9rem;
            }}
            .kpi-sublabel {{
                font-size: 0.8rem;
            }}
            .kpi-icon {{
                font-size: 2rem;
                top: 15px;
                right: 15px;
            }}
            .chart-card {{
                padding: 15px;
                border-radius: 16px;
            }}
            .chart-title {{
                font-size: 1rem;
                margin-bottom: 15px;
            }}
            .gauge-container {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}
            .gauge-label {{
                font-size: 0.8rem;
            }}
            .data-card {{
                padding: 20px;
                border-radius: 16px;
            }}
            .data-card-header {{
                font-size: 0.9rem;
            }}
            .data-card-value {{
                font-size: 1.6rem;
            }}
            .data-row {{
                font-size: 0.85rem;
            }}
            .table-container {{
                padding: 15px;
                border-radius: 16px;
                overflow-x: auto;
            }}
            .data-table th,
            .data-table td {{
                padding: 10px 8px;
                font-size: 0.8rem;
            }}
            .footer {{
                padding: 25px 15px;
                font-size: 0.75rem;
            }}
        }}

        /* Extra small phones */
        @media (max-width: 360px) {{
            .kpi-card.main .kpi-value {{
                font-size: 2.2rem;
            }}
            .kpi-value {{
                font-size: 2rem;
            }}
            .nav-btn {{
                padding: 8px 10px;
                font-size: 0.75rem;
            }}
        }}

        /* Hide elements based on language */
        .en-only {{ display: block; }}
        .ar-only {{ display: none; }}
        .rtl .en-only {{ display: none; }}
        .rtl .ar-only {{ display: block; }}

        /* ============================================
           KNOWLEDGE BASE TAB STYLES - MOBILE FIRST
           ============================================ */

        /* KB Header - Compact for mobile */
        .kb-header {{
            margin-bottom: 15px;
        }}

        .company-info-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .company-logo {{
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #22c55e 0%, #06b6d4 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 800;
            color: white;
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
            flex-shrink: 0;
        }}

        .company-details h2 {{
            font-size: 1rem;
            margin-bottom: 2px;
            background: linear-gradient(90deg, var(--white) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .company-details p {{
            color: var(--gray);
            font-size: 0.8rem;
        }}

        /* KB Controls - Stacked on mobile */
        .kb-controls {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .search-box {{
            position: relative;
            width: 100%;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 15px 12px 42px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 10px;
            color: var(--white);
            font-size: 0.95rem;
            font-family: inherit;
            outline: none;
            transition: all 0.3s ease;
        }}

        .search-box input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(14, 165, 233, 0.2);
        }}

        .search-box .search-icon {{
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1rem;
        }}

        .rtl .search-box .search-icon {{
            left: auto;
            right: 14px;
        }}

        .rtl .search-box input {{
            padding: 12px 42px 12px 15px;
        }}

        /* Unit Toggle - Full width on mobile */
        .unit-toggle {{
            display: flex;
            background: var(--glass);
            border-radius: 10px;
            padding: 3px;
            border: 1px solid var(--glass-border);
            width: 100%;
        }}

        .unit-btn {{
            flex: 1;
            padding: 10px 15px;
            border: none;
            background: transparent;
            color: var(--gray);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.3s ease;
            font-family: inherit;
        }}

        .unit-btn.active {{
            background: var(--primary);
            color: var(--white);
        }}

        /* Category Navigation - Horizontal scroll on mobile */
        .category-nav {{
            display: flex;
            gap: 8px;
            padding: 12px 0;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
            border-bottom: 1px solid var(--glass-border);
            margin-bottom: 15px;
        }}

        .category-nav::-webkit-scrollbar {{
            display: none;
        }}

        .cat-btn {{
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 10px 14px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 10px;
            color: var(--gray);
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: inherit;
            white-space: nowrap;
            flex-shrink: 0;
        }}

        .cat-btn:hover {{
            background: rgba(14, 165, 233, 0.15);
            border-color: var(--primary);
            color: var(--white);
        }}

        .cat-btn.active {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-color: transparent;
            color: var(--white);
        }}

        .cat-icon {{
            font-size: 1rem;
        }}

        .cat-count {{
            background: rgba(255,255,255,0.2);
            padding: 2px 6px;
            border-radius: 20px;
            font-size: 0.75rem;
        }}

        /* KB Cards Grid - Single column on mobile, cards first */
        .kb-cards-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            margin-bottom: 20px;
        }}

        /* Active filter indicator */
        .filter-indicator {{
            display: none;
            padding: 10px 15px;
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
            border: 1px solid var(--primary);
            border-radius: 10px;
            margin-bottom: 15px;
            font-size: 0.85rem;
            color: var(--secondary);
        }}

        .filter-indicator.visible {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .filter-indicator .clear-btn {{
            background: none;
            border: none;
            color: var(--gray);
            cursor: pointer;
            font-size: 1rem;
            padding: 2px 8px;
        }}

        /* Collapsible Charts Section - At bottom */
        .kb-charts-section {{
            margin-top: 25px;
            border-top: 1px solid var(--glass-border);
            padding-top: 15px;
        }}

        .charts-toggle {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 15px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            cursor: pointer;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }}

        .charts-toggle:hover {{
            border-color: var(--primary);
        }}

        .charts-toggle h3 {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--light);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .charts-toggle .toggle-arrow {{
            color: var(--gray);
            font-size: 1rem;
            transition: transform 0.3s ease;
        }}

        .charts-toggle.expanded .toggle-arrow {{
            transform: rotate(180deg);
        }}

        .kb-charts-content {{
            display: none;
            padding-top: 10px;
        }}

        .kb-charts-content.visible {{
            display: block;
        }}

        .kb-charts-content .chart-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }}

        .kb-charts-content .chart-card {{
            min-height: 280px;
        }}

        /* Collapsible Definitions Section */
        .definitions-section {{
            margin-top: 25px;
            padding-top: 15px;
            border-top: 1px solid var(--glass-border);
        }}

        .definitions-toggle {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 15px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            cursor: pointer;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }}

        .definitions-toggle:hover {{
            border-color: var(--secondary);
        }}

        .definitions-toggle h3 {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--light);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .definitions-toggle .toggle-arrow {{
            color: var(--gray);
            font-size: 1rem;
            transition: transform 0.3s ease;
        }}

        .definitions-toggle.expanded .toggle-arrow {{
            transform: rotate(180deg);
        }}

        .definitions-content {{
            display: none;
        }}

        .definitions-content.visible {{
            display: block;
        }}

        /* Desktop adjustments */
        @media (min-width: 768px) {{
            .company-info-card {{
                padding: 20px;
                gap: 20px;
            }}

            .company-logo {{
                width: 60px;
                height: 60px;
                font-size: 28px;
            }}

            .company-details h2 {{
                font-size: 1.2rem;
            }}

            .kb-controls {{
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }}

            .search-box {{
                max-width: 350px;
            }}

            .unit-toggle {{
                width: auto;
            }}

            .kb-cards-grid {{
                grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
                gap: 15px;
            }}

            .kb-charts-content .chart-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (min-width: 1024px) {{
            .company-info-card {{
                padding: 25px;
            }}

            .company-logo {{
                width: 70px;
                height: 70px;
                font-size: 32px;
            }}

            .company-details h2 {{
                font-size: 1.3rem;
            }}

            .kb-cards-grid {{
                grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            }}
        }}

        /* KB Card - Mobile first */
        .kb-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .kb-card:hover {{
            border-color: var(--primary);
            box-shadow: 0 5px 20px rgba(14, 165, 233, 0.15);
        }}

        .kb-card.hidden {{
            display: none;
        }}

        .kb-card-header {{
            display: flex;
            align-items: center;
            padding: 12px 14px;
            cursor: pointer;
            gap: 10px;
            border-bottom: 1px solid transparent;
            transition: all 0.3s ease;
        }}

        .kb-card.expanded .kb-card-header {{
            border-bottom-color: var(--glass-border);
        }}

        .kb-card-icon {{
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            flex-shrink: 0;
        }}

        .kb-card-title {{
            flex: 1;
            min-width: 0;
        }}

        .kb-card-title h3 {{
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .kb-card-subtitle {{
            font-size: 0.7rem;
            color: var(--gray);
        }}

        .kb-card-summary {{
            text-align: right;
            flex-shrink: 0;
        }}

        .rtl .kb-card-summary {{
            text-align: left;
        }}

        .summary-value {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 1px;
        }}

        .rtl .summary-value {{
            align-items: flex-start;
        }}

        .summary-value .design-value {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--secondary);
        }}

        .summary-value .actual-value {{
            font-size: 0.75rem;
            color: var(--success);
        }}

        .summary-value .unit {{
            font-size: 0.65rem;
            color: var(--gray);
        }}

        .kb-card-expand {{
            width: 26px;
            height: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .expand-icon {{
            transition: transform 0.3s ease;
            color: var(--gray);
            font-size: 0.9rem;
        }}

        .kb-card.expanded .expand-icon {{
            transform: rotate(180deg);
        }}

        /* Card Body */
        .kb-card-body {{
            display: none;
            padding: 14px;
            animation: slideDown 0.3s ease;
        }}

        .kb-card.expanded .kb-card-body {{
            display: block;
        }}

        @keyframes slideDown {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Capacity Section */
        .capacity-section {{
            margin-bottom: 15px;
            padding: 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }}

        .capacity-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
            font-size: 0.85rem;
        }}

        .capacity-row .label {{
            color: var(--gray);
        }}

        .capacity-row .value.design {{
            color: var(--secondary);
            font-weight: 600;
        }}

        .capacity-row .value.actual {{
            color: var(--success);
            font-weight: 600;
        }}

        .capacity-bar {{
            height: 6px;
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
            margin-top: 8px;
            overflow: hidden;
        }}

        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--success) 0%, var(--secondary) 100%);
            border-radius: 3px;
            transition: width 0.5s ease;
        }}

        /* Desktop card adjustments */
        @media (min-width: 768px) {{
            .kb-card-header {{
                padding: 15px 18px;
                gap: 12px;
            }}

            .kb-card-icon {{
                width: 45px;
                height: 45px;
                font-size: 1.2rem;
            }}

            .kb-card-title h3 {{
                font-size: 0.95rem;
            }}

            .summary-value .design-value {{
                font-size: 1.1rem;
            }}

            .kb-card-body {{
                padding: 18px;
            }}
        }}

        /* Composition Section */
        .composition-section, .conditions-section, .routing-section, .special-section {{
            margin-bottom: 20px;
        }}

        .composition-section h4, .conditions-section h4, .routing-section h4, .special-section h4 {{
            font-size: 0.9rem;
            color: var(--gray);
            margin-bottom: 10px;
        }}

        .comp-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .comp-list li {{
            padding: 6px 0;
            border-bottom: 1px dashed rgba(255,255,255,0.1);
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
        }}

        .comp-list li:last-child {{
            border-bottom: none;
        }}

        .comp-name {{
            color: var(--gray);
        }}

        .comp-val {{
            color: var(--white);
            font-weight: 500;
        }}

        .comp-chart {{
            margin-top: 15px;
            height: 180px;
        }}

        /* Conditions Grid */
        .conditions-grid {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}

        .condition-item {{
            background: rgba(14, 165, 233, 0.1);
            padding: 10px 15px;
            border-radius: 8px;
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        .cond-label {{
            font-weight: 600;
            color: var(--secondary);
        }}

        .cond-value {{
            color: var(--white);
        }}

        /* Routing Section */
        .routing-flow {{
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }}

        .route-node {{
            padding: 12px 18px;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 500;
        }}

        .route-node.source {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: #f59e0b;
        }}

        .route-node.destination {{
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #22c55e;
        }}

        .route-arrow {{
            font-size: 1.5rem;
            color: var(--gray);
        }}

        /* Definition Toggle */
        .definition-toggle {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 15px;
            background: rgba(138, 92, 246, 0.1);
            border: 1px solid rgba(138, 92, 246, 0.2);
            border-radius: 10px;
            cursor: pointer;
            margin-bottom: 10px;
            transition: all 0.3s ease;
        }}

        .definition-toggle:hover {{
            background: rgba(138, 92, 246, 0.15);
        }}

        .toggle-icon {{
            font-size: 1.2rem;
            color: var(--gray);
            transition: transform 0.3s ease;
        }}

        .definition-toggle.expanded .toggle-icon {{
            transform: rotate(45deg);
        }}

        .definition-content {{
            padding: 0 15px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease, padding 0.3s ease;
        }}

        .definition-toggle.expanded + .definition-content {{
            max-height: 300px;
            padding: 15px;
        }}

        .simple-def {{
            color: var(--secondary);
            font-weight: 500;
            margin-bottom: 10px;
        }}

        .detailed-def {{
            color: var(--gray);
            font-size: 0.9rem;
            line-height: 1.6;
            display: none;
        }}

        .definition-toggle.expanded + .definition-content .detailed-def {{
            display: block;
        }}

        /* Comments Section */
        .comments-section {{
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            border-left: 3px solid var(--accent);
            margin-top: 15px;
        }}

        .rtl .comments-section {{
            border-left: none;
            border-right: 3px solid var(--accent);
        }}

        .comments-section h4 {{
            font-size: 0.85rem;
            color: var(--gray);
            margin-bottom: 8px;
        }}

        .comments-section p {{
            font-size: 0.9rem;
            color: var(--light);
            line-height: 1.5;
        }}

        /* Definitions Section */
        .definitions-section {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid var(--glass-border);
        }}

        .definitions-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
        }}

        .def-card {{
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .def-card:hover {{
            border-color: var(--secondary);
        }}

        .def-card.expanded {{
            border-color: var(--primary);
        }}

        .def-term {{
            font-weight: 600;
            color: var(--secondary);
            margin-bottom: 5px;
        }}

        .def-simple {{
            font-size: 0.9rem;
            color: var(--light);
        }}

        .def-detailed {{
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px dashed var(--glass-border);
            font-size: 0.85rem;
            color: var(--gray);
            line-height: 1.5;
            display: none;
        }}

        /* Mobile routing */
        @media (max-width: 480px) {{
            .routing-flow {{
                flex-direction: column;
                align-items: stretch;
                gap: 8px;
            }}

            .route-arrow {{
                transform: rotate(90deg);
                align-self: center;
            }}

            .route-node {{
                text-align: center;
                padding: 10px 14px;
                font-size: 0.85rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="bg-animation"></div>

    <header class="header">
        <div class="logo">
            <div class="logo-icon">M</div>
            <div class="logo-text">
                <h1 class="en-only">MIDOR-ETHYDCO Integration</h1>
                <h1 class="ar-only">تكامل ميدور وإيثيدكو</h1>
                <span class="en-only">Petrochemical Integration Analysis</span>
                <span class="ar-only">تحليل التكامل البتروكيماوي</span>
            </div>
        </div>
        <div class="lang-toggle">
            <button class="lang-btn active" onclick="setLanguage('en')">English</button>
            <button class="lang-btn" onclick="setLanguage('ar')">العربية</button>
        </div>
    </header>

    <nav class="nav">
        <button class="nav-btn active" onclick="showTab('overview')">
            <span class="en-only">Overview</span>
            <span class="ar-only">نظرة عامة</span>
        </button>
        <button class="nav-btn" onclick="showTab('financial')">
            <span class="en-only">Financial Analysis</span>
            <span class="ar-only">التحليل المالي</span>
        </button>
        <button class="nav-btn" onclick="showTab('process')">
            <span class="en-only">Process Flow</span>
            <span class="ar-only">تدفق العمليات</span>
        </button>
        <button class="nav-btn" onclick="showTab('detailed')">
            <span class="en-only">Detailed Data</span>
            <span class="ar-only">البيانات التفصيلية</span>
        </button>
        <button class="nav-btn" onclick="showTab('knowledge')">
            <span class="en-only">ETHYDCO Knowledge Base</span>
            <span class="ar-only">قاعدة معرفة إيثيدكو</span>
        </button>
    </nav>

    <main class="content">
        <!-- OVERVIEW TAB -->
        <div id="overview" class="tab-content active">
            <div class="kpi-section">
                <div class="kpi-card main">
                    <div class="kpi-label en-only">Total Annual Integration Value</div>
                    <div class="kpi-label ar-only">إجمالي قيمة التكامل السنوية</div>
                    <div class="kpi-value">${total_value/1e6:.0f}M</div>
                    <div class="kpi-sublabel en-only">Net value after all costs</div>
                    <div class="kpi-sublabel ar-only">القيمة الصافية بعد جميع التكاليف</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon">⚡</div>
                    <div class="kpi-label en-only">Phase 1+2: Gas Recovery</div>
                    <div class="kpi-label ar-only">المرحلة 1+2: استرداد الغاز</div>
                    <div class="kpi-value">${phase12/1e6:.0f}M</div>
                    <div class="kpi-sublabel en-only">LPG, H2, C2, C5+ Recovery</div>
                    <div class="kpi-sublabel ar-only">استرداد الغاز المسال والهيدروجين</div>
                </div>
                <div class="kpi-card accent">
                    <div class="kpi-icon">🧪</div>
                    <div class="kpi-label en-only">Phase 3+4: Methanol & MTO</div>
                    <div class="kpi-label ar-only">المرحلة 3+4: الميثانول</div>
                    <div class="kpi-value">${phase34/1e6:.0f}M</div>
                    <div class="kpi-sublabel en-only">Methanol Blending & Olefins</div>
                    <div class="kpi-sublabel ar-only">مزج الميثانول والأوليفينات</div>
                </div>
            </div>

            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">Value Distribution</span>
                        <span class="ar-only">توزيع القيمة</span>
                    </div>
                    <div id="chart-donut-en"></div>
                    <div id="chart-donut-ar"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">Product Values</span>
                        <span class="ar-only">قيم المنتجات</span>
                    </div>
                    <div id="chart-products-en"></div>
                    <div id="chart-products-ar"></div>
                </div>
            </div>
        </div>

        <!-- FINANCIAL TAB -->
        <div id="financial" class="tab-content">
            <div class="chart-grid">
                <div class="chart-card full">
                    <div class="chart-title">
                        <span class="en-only">Cost-Benefit Analysis</span>
                        <span class="ar-only">تحليل التكلفة والعائد</span>
                    </div>
                    <div id="chart-costbenefit-en"></div>
                    <div id="chart-costbenefit-ar"></div>
                </div>
            </div>

            <div class="table-container">
                <div class="chart-title">
                    <span class="en-only">Financial Summary</span>
                    <span class="ar-only">الملخص المالي</span>
                </div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th class="en-only">Product</th>
                            <th class="ar-only">المنتج</th>
                            <th class="en-only">Quantity (t/y)</th>
                            <th class="ar-only">الكمية (طن/سنة)</th>
                            <th class="en-only">Value ($/y)</th>
                            <th class="ar-only">القيمة ($/سنة)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>LPG (C3+C4)</td>
                            <td>{metrics['calc1']['total_LPG']:,.0f}</td>
                            <td class="value">${metrics['calc1']['LPG_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>C5+ (Naphtha)</td>
                            <td>{metrics['calc1']['total_C5+']:,.0f}</td>
                            <td class="value">${metrics['calc1']['C5+_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Hydrogen (H2)</td>
                            <td>{metrics['calc2']['total_H2']:,.0f}</td>
                            <td class="value">${metrics['calc2']['H2_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Ethane (C2)</td>
                            <td>{metrics['calc3']['MIDOR_C2_supply']:,.0f}</td>
                            <td class="value">${metrics['calc3']['C2_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Methanol Blend</td>
                            <td>{metrics['calc6']['methanol_in_gasoline']:,.0f}</td>
                            <td class="value">${metrics['calc6']['methanol_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Ethylene (MTO)</td>
                            <td>{metrics['calc6']['ethylene_from_MTO']:,.0f}</td>
                            <td class="value">${metrics['calc6']['ethylene_value']:,.0f}</td>
                        </tr>
                        <tr>
                            <td>Propylene (MTO)</td>
                            <td>{metrics['calc6']['propylene_from_MTO']:,.0f}</td>
                            <td class="value">${metrics['calc6']['propylene_value']:,.0f}</td>
                        </tr>
                        <tr style="background: rgba(239,68,68,0.1);">
                            <td><strong class="en-only">NG Makeup Cost</strong><strong class="ar-only">تكلفة الغاز الطبيعي</strong></td>
                            <td>-</td>
                            <td class="cost">-${metrics['summary']['phase12_NG_cost']:,.0f}</td>
                        </tr>
                        <tr style="background: rgba(34,197,94,0.2);">
                            <td><strong class="en-only">TOTAL NET VALUE</strong><strong class="ar-only">إجمالي القيمة الصافية</strong></td>
                            <td>-</td>
                            <td class="value"><strong>${metrics['summary']['total_net']:,.0f}</strong></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- PROCESS TAB -->
        <div id="process" class="tab-content">
            <div class="chart-grid">
                <div class="chart-card full">
                    <div class="chart-title">
                        <span class="en-only">Material & Value Flow</span>
                        <span class="ar-only">تدفق المواد والقيمة</span>
                    </div>
                    <div id="chart-sankey-en"></div>
                    <div id="chart-sankey-ar"></div>
                </div>
            </div>

            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">ETHYDCO C2 Feed Coverage</span>
                        <span class="ar-only">تغطية تغذية الإيثان لإيثيدكو</span>
                    </div>
                    <div class="gauge-container">
                        <div class="gauge-card">
                            <div id="chart-gauge-min-en"></div>
                            <div id="chart-gauge-min-ar"></div>
                            <div class="gauge-label en-only">Min Demand Coverage</div>
                            <div class="gauge-label ar-only">تغطية الحد الأدنى</div>
                        </div>
                        <div class="gauge-card">
                            <div id="chart-gauge-max-en"></div>
                            <div id="chart-gauge-max-ar"></div>
                            <div class="gauge-label en-only">Max Demand Coverage</div>
                            <div class="gauge-label ar-only">تغطية الحد الأقصى</div>
                        </div>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">H2 Balance for Methanol</span>
                        <span class="ar-only">توازن الهيدروجين للميثانول</span>
                    </div>
                    <div id="chart-h2-en"></div>
                    <div id="chart-h2-ar"></div>
                </div>
            </div>

            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">Stream Component Distribution</span>
                        <span class="ar-only">توزيع مكونات التيارات</span>
                    </div>
                    <div id="chart-heatmap-en"></div>
                    <div id="chart-heatmap-ar"></div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">
                        <span class="en-only">Methanol Allocation</span>
                        <span class="ar-only">توزيع الميثانول</span>
                    </div>
                    <div id="chart-methanol-en"></div>
                    <div id="chart-methanol-ar"></div>
                </div>
            </div>
        </div>

        <!-- DETAILED TAB -->
        <div id="detailed" class="tab-content">
            <div class="chart-title" style="margin-bottom: 20px; font-size: 1.3rem;">
                <span class="en-only">Stream Details</span>
                <span class="ar-only">تفاصيل التيارات</span>
            </div>

            <div class="data-grid">
                {stream_cards_html}
            </div>

            <div class="table-container" style="margin-top: 30px;">
                <div class="chart-title">
                    <span class="en-only">Product Prices</span>
                    <span class="ar-only">أسعار المنتجات</span>
                </div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th class="en-only">Product</th>
                            <th class="ar-only">المنتج</th>
                            <th class="en-only">Price ($/ton)</th>
                            <th class="ar-only">السعر ($/طن)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {prices_table_html}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- KNOWLEDGE BASE TAB -->
        <div id="knowledge" class="tab-content">
            <!-- Header Section with Company Info -->
            <div class="kb-header">
                <div class="company-info-card">
                    <div class="company-logo">E</div>
                    <div class="company-details">
                        <h2 class="en-only">{company_name} - {company_full}</h2>
                        <h2 class="ar-only">{ethydco_data['company_info']['name_ar']} - {ethydco_data['company_info']['full_name_ar']}</h2>
                        <p class="en-only">{company_scope}</p>
                        <p class="ar-only">{ethydco_data['company_info']['scope_ar']}</p>
                    </div>
                </div>

                <!-- Controls Row -->
                <div class="kb-controls">
                    <!-- Search Box -->
                    <div class="search-box">
                        <input type="text" id="kb-search" placeholder="Search streams, products..." oninput="filterKB()">
                        <span class="search-icon">🔍</span>
                    </div>

                    <!-- Unit Toggle -->
                    <div class="unit-toggle">
                        <button class="unit-btn active" onclick="setUnit('hourly')" data-unit="hourly">T/hr</button>
                        <button class="unit-btn" onclick="setUnit('annual')" data-unit="annual">T/year</button>
                    </div>
                </div>
            </div>

            <!-- Category Navigation -->
            <div class="category-nav">
                <button class="cat-btn active" onclick="filterCategory('all')" data-cat="all">
                    <span class="en-only">All</span>
                    <span class="ar-only">الكل</span>
                    <span class="cat-count" id="count-all">17</span>
                </button>
                <button class="cat-btn" onclick="filterCategory('feeds')" data-cat="feeds">
                    <span class="cat-icon">⚡</span>
                    <span class="en-only">Feeds</span>
                    <span class="ar-only">التغذية</span>
                    <span class="cat-count" id="count-feeds">4</span>
                </button>
                <button class="cat-btn" onclick="filterCategory('products')" data-cat="products">
                    <span class="cat-icon">📦</span>
                    <span class="en-only">Products</span>
                    <span class="ar-only">المنتجات</span>
                    <span class="cat-count" id="count-products">7</span>
                </button>
                <button class="cat-btn" onclick="filterCategory('flares')" data-cat="flares">
                    <span class="cat-icon">🔥</span>
                    <span class="en-only">Flares</span>
                    <span class="ar-only">الشعلات</span>
                    <span class="cat-count" id="count-flares">2</span>
                </button>
                <button class="cat-btn" onclick="filterCategory('fuel')" data-cat="fuel">
                    <span class="cat-icon">⛽</span>
                    <span class="en-only">Fuel Gas</span>
                    <span class="ar-only">غاز الوقود</span>
                    <span class="cat-count" id="count-fuel">3</span>
                </button>
                <button class="cat-btn" onclick="filterCategory('other')" data-cat="other">
                    <span class="cat-icon">🌀</span>
                    <span class="en-only">Other</span>
                    <span class="ar-only">أخرى</span>
                    <span class="cat-count" id="count-other">1</span>
                </button>
            </div>

            <!-- Filter Indicator -->
            <div class="filter-indicator" id="filter-indicator">
                <span id="filter-text"></span>
                <button class="clear-btn" onclick="clearFilters()">✕</button>
            </div>

            <!-- CARDS FIRST - Primary Content -->
            <div class="kb-cards-grid" id="kb-cards-container">
                {kb_cards_html}
            </div>

            <!-- Collapsible Charts Section - AT BOTTOM -->
            <div class="kb-charts-section">
                <div class="charts-toggle" onclick="toggleChartsSection(this)">
                    <h3>
                        <span>📊</span>
                        <span class="en-only">Charts & Visualizations</span>
                        <span class="ar-only">الرسوم البيانية</span>
                    </h3>
                    <span class="toggle-arrow">▼</span>
                </div>
                <div class="kb-charts-content" id="kb-charts-content">
                    <div class="chart-grid">
                        <div class="chart-card">
                            <div class="chart-title">
                                <span class="en-only">Design vs Actual Capacity</span>
                                <span class="ar-only">السعة التصميمية مقابل الفعلية</span>
                            </div>
                            <div id="chart-kb-design-en"></div>
                            <div id="chart-kb-design-ar"></div>
                        </div>
                        <div class="chart-card">
                            <div class="chart-title">
                                <span class="en-only">ETHYDCO Process Flow</span>
                                <span class="ar-only">مسار العمليات في إيثيدكو</span>
                            </div>
                            <div id="chart-kb-routing-en"></div>
                            <div id="chart-kb-routing-ar"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Collapsible Definitions Section - AT BOTTOM -->
            <div class="definitions-section">
                <div class="definitions-toggle" onclick="toggleDefinitionsSection(this)">
                    <h3>
                        <span>📖</span>
                        <span class="en-only">Glossary / Definitions</span>
                        <span class="ar-only">المصطلحات والتعريفات</span>
                    </h3>
                    <span class="toggle-arrow">▼</span>
                </div>
                <div class="definitions-content" id="definitions-content">
                    <div class="definitions-grid" id="definitions-container">
                        {definitions_html}
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <span class="en-only">MIDOR-ETHYDCO Integration Analysis | Generated: {pd.Timestamp.now().strftime('%Y-%m-%d')}</span>
        <span class="ar-only">تحليل التكامل بين ميدور وإيثيدكو | تاريخ الإنشاء: {pd.Timestamp.now().strftime('%Y-%m-%d')}</span>
    </footer>

    <script>
        // Chart data
        var chartsEN = {{
            donut: {charts['en']['donut'].to_json()},
            products: {charts['en']['products'].to_json()},
            costbenefit: {charts['en']['cost_benefit'].to_json()},
            sankey: {charts['en']['sankey'].to_json()},
            gaugeMin: {charts['en']['gauge_min'].to_json()},
            gaugeMax: {charts['en']['gauge_max'].to_json()},
            h2: {charts['en']['h2_balance'].to_json()},
            heatmap: {charts['en']['heatmap'].to_json()},
            methanol: {charts['en']['methanol'].to_json()},
            kbDesign: {charts['en']['kb_design_actual'].to_json()},
            kbRouting: {charts['en']['kb_routing'].to_json()}
        }};

        var chartsAR = {{
            donut: {charts['ar']['donut'].to_json()},
            products: {charts['ar']['products'].to_json()},
            costbenefit: {charts['ar']['cost_benefit'].to_json()},
            sankey: {charts['ar']['sankey'].to_json()},
            gaugeMin: {charts['ar']['gauge_min'].to_json()},
            gaugeMax: {charts['ar']['gauge_max'].to_json()},
            h2: {charts['ar']['h2_balance'].to_json()},
            heatmap: {charts['ar']['heatmap'].to_json()},
            methanol: {charts['ar']['methanol'].to_json()},
            kbDesign: {charts['ar']['kb_design_actual'].to_json()},
            kbRouting: {charts['ar']['kb_routing'].to_json()}
        }};

        var config = {{responsive: true, displayModeBar: false}};
        var currentLang = 'en';
        var currentCategory = 'all';
        var currentUnit = 'hourly';
        var OPERATING_HOURS = 8000;

        function renderCharts(lang) {{
            var charts = lang === 'ar' ? chartsAR : chartsEN;
            var suffix = '-' + lang;
            var otherSuffix = lang === 'ar' ? '-en' : '-ar';

            // Hide other language charts
            document.querySelectorAll('[id$="' + otherSuffix + '"]').forEach(el => el.style.display = 'none');
            document.querySelectorAll('[id$="' + suffix + '"]').forEach(el => el.style.display = 'block');

            Plotly.newPlot('chart-donut' + suffix, charts.donut.data, charts.donut.layout, config);
            Plotly.newPlot('chart-products' + suffix, charts.products.data, charts.products.layout, config);
            Plotly.newPlot('chart-costbenefit' + suffix, charts.costbenefit.data, charts.costbenefit.layout, config);
            Plotly.newPlot('chart-sankey' + suffix, charts.sankey.data, charts.sankey.layout, config);
            Plotly.newPlot('chart-gauge-min' + suffix, charts.gaugeMin.data, charts.gaugeMin.layout, config);
            Plotly.newPlot('chart-gauge-max' + suffix, charts.gaugeMax.data, charts.gaugeMax.layout, config);
            Plotly.newPlot('chart-h2' + suffix, charts.h2.data, charts.h2.layout, config);
            Plotly.newPlot('chart-heatmap' + suffix, charts.heatmap.data, charts.heatmap.layout, config);
            Plotly.newPlot('chart-methanol' + suffix, charts.methanol.data, charts.methanol.layout, config);

            // KB Charts
            var kbDesignEl = document.getElementById('chart-kb-design' + suffix);
            var kbRoutingEl = document.getElementById('chart-kb-routing' + suffix);
            if (kbDesignEl) {{
                Plotly.newPlot('chart-kb-design' + suffix, charts.kbDesign.data, charts.kbDesign.layout, config);
            }}
            if (kbRoutingEl) {{
                Plotly.newPlot('chart-kb-routing' + suffix, charts.kbRouting.data, charts.kbRouting.layout, config);
            }}
        }}

        function setLanguage(lang) {{
            currentLang = lang;
            document.body.classList.toggle('rtl', lang === 'ar');

            // Update toggle buttons
            document.querySelectorAll('.lang-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.textContent.includes(lang === 'ar' ? 'العربية' : 'English'));
            }});

            renderCharts(lang);
            window.dispatchEvent(new Event('resize'));
        }}

        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));

            document.getElementById(tabId).classList.add('active');
            event.target.closest('.nav-btn').classList.add('active');

            setTimeout(() => {{
                window.dispatchEvent(new Event('resize'));
                if (tabId === 'knowledge') {{
                    renderCharts(currentLang);
                }}
            }}, 100);
        }}

        // ============================================
        // KNOWLEDGE BASE FUNCTIONS
        // ============================================

        function toggleCard(header) {{
            var card = header.closest('.kb-card');
            card.classList.toggle('expanded');
        }}

        function toggleDefCard(card) {{
            var detailed = card.querySelector('.def-detailed');
            if (detailed) {{
                var isExpanded = detailed.style.display === 'block';
                detailed.style.display = isExpanded ? 'none' : 'block';
                card.classList.toggle('expanded', !isExpanded);
            }}
        }}

        // Toggle collapsible charts section
        function toggleChartsSection(toggle) {{
            toggle.classList.toggle('expanded');
            var content = document.getElementById('kb-charts-content');
            content.classList.toggle('visible');
            if (content.classList.contains('visible')) {{
                setTimeout(() => {{
                    window.dispatchEvent(new Event('resize'));
                    renderCharts(currentLang);
                }}, 100);
            }}
        }}

        // Toggle collapsible definitions section
        function toggleDefinitionsSection(toggle) {{
            toggle.classList.toggle('expanded');
            var content = document.getElementById('definitions-content');
            content.classList.toggle('visible');
        }}

        function filterCategory(category) {{
            currentCategory = category;

            // Update category buttons
            document.querySelectorAll('.cat-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.dataset.cat === category);
            }});

            // Apply filter and update indicator
            applyFilters();
            updateFilterIndicator();
        }}

        function filterKB() {{
            applyFilters();
            updateFilterIndicator();
        }}

        function clearFilters() {{
            currentCategory = 'all';
            document.getElementById('kb-search').value = '';
            document.querySelectorAll('.cat-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.dataset.cat === 'all');
            }});
            applyFilters();
            updateFilterIndicator();
        }}

        function updateFilterIndicator() {{
            var indicator = document.getElementById('filter-indicator');
            var filterText = document.getElementById('filter-text');
            var searchTerm = document.getElementById('kb-search').value;

            var hasFilter = currentCategory !== 'all' || searchTerm;
            indicator.classList.toggle('visible', hasFilter);

            if (hasFilter) {{
                var parts = [];
                if (currentCategory !== 'all') {{
                    var catNames = {{ feeds: 'Feeds', products: 'Products', flares: 'Flares', fuel: 'Fuel Gas', other: 'Other' }};
                    parts.push(catNames[currentCategory] || currentCategory);
                }}
                if (searchTerm) {{
                    parts.push('"' + searchTerm + '"');
                }}
                filterText.textContent = 'Showing: ' + parts.join(' + ');
            }}
        }}

        function applyFilters() {{
            var searchTerm = (document.getElementById('kb-search').value || '').toLowerCase();
            var cards = document.querySelectorAll('.kb-card');
            var counts = {{ all: 0, feeds: 0, products: 0, flares: 0, fuel: 0, other: 0 }};
            var visibleCount = 0;

            cards.forEach(card => {{
                var category = card.dataset.category;
                var text = card.textContent.toLowerCase();

                var categoryMatch = currentCategory === 'all' || category === currentCategory;
                var searchMatch = !searchTerm || text.includes(searchTerm);

                var visible = categoryMatch && searchMatch;
                card.classList.toggle('hidden', !visible);

                if (visible) {{
                    visibleCount++;
                    counts.all++;
                    if (counts[category] !== undefined) counts[category]++;
                }}
            }});

            // Update counts
            Object.keys(counts).forEach(cat => {{
                var el = document.getElementById('count-' + cat);
                if (el) el.textContent = counts[cat];
            }});

            // Scroll to cards if filtering
            if (currentCategory !== 'all' || searchTerm) {{
                var cardsContainer = document.getElementById('kb-cards-container');
                if (cardsContainer && visibleCount > 0) {{
                    cardsContainer.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }}
        }}

        function setUnit(unit) {{
            currentUnit = unit;

            // Update unit buttons
            document.querySelectorAll('.unit-btn').forEach(btn => {{
                btn.classList.toggle('active', btn.dataset.unit === unit);
            }});

            // Update displayed values
            updateUnitDisplay();
        }}

        function updateUnitDisplay() {{
            document.querySelectorAll('.kb-card').forEach(card => {{
                var designVal = parseFloat(card.dataset.designValue);
                var designUnit = card.dataset.designUnit || '';
                var actualVal = parseFloat(card.dataset.actualValue);
                var actualUnit = card.dataset.actualUnit || designUnit;

                if (isNaN(designVal) && isNaN(actualVal)) return;

                var designDisplay = card.querySelector('.summary-value .design-value');
                var actualDisplay = card.querySelector('.summary-value .actual-value');
                var unitDisplay = card.querySelector('.summary-value .unit');

                if (currentUnit === 'annual') {{
                    // Convert to annual
                    var annualDesign = convertToAnnual(designVal, designUnit);
                    var annualActual = convertToAnnual(actualVal, actualUnit);

                    if (designDisplay && !isNaN(annualDesign)) {{
                        designDisplay.textContent = formatNumber(annualDesign);
                    }}
                    if (actualDisplay && !isNaN(annualActual)) {{
                        actualDisplay.textContent = formatNumber(annualActual);
                    }}
                    if (unitDisplay) unitDisplay.textContent = 'T/year';
                }} else {{
                    // Show original hourly values
                    if (designDisplay && !isNaN(designVal)) {{
                        designDisplay.textContent = formatNumber(designVal);
                    }}
                    if (actualDisplay && !isNaN(actualVal)) {{
                        actualDisplay.textContent = formatNumber(actualVal);
                    }}
                    if (unitDisplay) unitDisplay.textContent = designUnit;
                }}
            }});
        }}

        function convertToAnnual(value, unit) {{
            if (isNaN(value)) return NaN;
            if (unit.includes('Year')) return value;
            if (unit.includes('Kg')) return value * OPERATING_HOURS / 1000;
            return value * OPERATING_HOURS; // T/hr -> T/year
        }}

        function formatNumber(num) {{
            if (isNaN(num)) return 'N/A';
            if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
            return num.toFixed(1);
        }}

        // Initial render
        renderCharts('en');
    </script>
</body>
</html>
'''

    return html

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("Loading metrics...")
    metrics = load_metrics()

    print("Generating modern dashboard...")
    html = generate_html(metrics)

    print("Writing HTML file...")
    with open('integration_dashboard_v2.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("\n" + "="*60)
    print("Dashboard V2 generated successfully!")
    print("="*60)
    print("\nOutput: integration_dashboard_v2.html")
    print("\nFeatures:")
    print("  - Modern dark glassmorphism design")
    print("  - Language toggle (English/Arabic)")
    print("  - Animated background")
    print("  - Responsive layout")
    print("  - Clean, readable charts")

if __name__ == '__main__':
    main()
