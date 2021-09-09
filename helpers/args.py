from optparse import OptionParser

parser = OptionParser()

parser.add_option("--mode")
parser.add_option("--generate_chart", default= 0)
parser.add_option("--backtesting", default= 0)

params, args = parser.parse_args()

