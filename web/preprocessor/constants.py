TEMPLATES_DIR = 'web/preprocessor/templates/'

SPREADERS = ['description']

REGEX_MAP = {
	"float": "[-+]?\d*\.\d+|$",
	# "float"
	# [-+] # option magnitude sign
	# ?\d*\.\d+ # should always contain starting digit(s) with decimal followed by some more digit(s)
	# 
	"int": "[-]?[0-9]+|$"
	# "int"
	# [-] # option for negative sign
	# ?[0-9]+ # can contain one or more digits
	# 
}