from verb_category_class import VerbCategory
from functions import convert_file_ext_to_json

verb_dict = VerbCategory.load_verb_dict("verbs_bloom_updated.json")
# print(verb_dict)
# filename = VerbCategory.get_filename_verbs_txt()
# VerbCategory.set_num_of_categories_from_file(filename)
# VerbCategory.confirm_num_of_categories()
# category_names = VerbCategory.get_category_names(filename)
# print(category_names)

VCs = VerbCategory.dict_to_object_list(verb_dict)
verb_dict = VerbCategory.object_list_to_dict(VCs)
print(verb_dict)
for VC in VCs:
    print(len(VC))

