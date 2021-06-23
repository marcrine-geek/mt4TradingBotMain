import re


# examples 
example1 = """
GOLD sell 1780
:fire:TP1: 1774
:fire:TP2: 1770
:fire:TP 3:1765
:fire:SL: 1792:see_no_evil:

"""

example2 = """
Gold sell 1771:sunglasses:

Tp1755

SL 1780

"""
example3 = """
Gold sell 1782

Tp1770

SL 1790

"""

example4 = """
BUY 1.39950 EURUSD EURUSD
takeProfit-1.39850
take profit @1.2345
TAKE PROFIT 1234568
TP-1.39750
TP 1.39650
TP 1.39550
TP 1.39450

SL 1.40750

"""

example5 = """
SELL GBPUSD

Entry price 1.38950

TP1 1.38750 :dart: 20 Pips 
TP2 1.38450:dart: 50 Pips 
TP3 1.37950 :dart: 100 Pips 

SL 1.39250 :no_entry: 30 Pips 
"""


def extractSymbol(rsignal):
    """
    This function takes the raw signal and returns symbol
    """
    for i in rsignal:
        parser = re.search(r"GBP\w+|USD\w+|EUR\w+|NZD\w+|CAD\w+|JPY\w+|AUD\w+", i,  flags=re.IGNORECASE)

        if bool(parser)==True:
            parser_span = parser.span()
            symbol = parser.string[parser_span[0]:parser_span[1]]
            return symbol
            break

def extractSide(rsignal):
    """
    This function takes the input signal and  returns the side
    """
    for i in rsignal: 
        parser = re.search(r"BUY|SELL|Sell|sell", i,  flags=re.IGNORECASE)
        if bool(parser) == True:
            parser_span = parser.span()
            side = parser.string[parser_span[0]:parser_span[1]]
            return side
            break

def extractTps(rsignal):
    """
    This function takes the raw signal and returns a list of takeprofits extracted from the signal
    """
    take_profit = []
    for i in rsignal: 
        parser = re.search(r"(TAKEPROFIT|TP|TP\d+)(\s|[at@\s]|[\d]|[,-]|[0-9])(\d+\.\d+)", i,  flags=re.IGNORECASE)
        if bool(parser) == True:
            parser_span = parser.span()
            tpstring = parser.string[parser_span[0]:parser_span[1]]
            tp_parse = re.findall(r'\d+\.\d+', tpstring, flags=re.IGNORECASE)
            for tp in tp_parse:
                take_profit.append(float(tp))
    return sorted(take_profit)            

       
def extractSls(rsignal):
    """
    This function takes the raw signal and returns a list of takeprofits extracted from the signal
    """
    stop_loss = []
    for i in rsignal: 
        parser = re.search(r"(STOPLOSS|SL|SL\d+)(\s|[at@\s]|[\d]|[,-]|[0-9])(\d+\.\d+)", i,  flags=re.IGNORECASE)
        if bool(parser) == True:
            parser_span = parser.span()
            slstring = parser.string[parser_span[0]:parser_span[1]]
            sl_parse = re.findall(r'\d+\.\d+', slstring, flags=re.IGNORECASE)
            for sl in sl_parse:
                stop_loss.append(float(sl))
    return sorted(stop_loss)     


rsignal = example5.split("\n")
        
def extractEP(rsignal):
    entry_price = []
    for i in rsignal:
        print("printing i", i)
        parser = re.search(r"(ENTRY)(\s|[at@\s]|[\d]|[,-]|[0-9])([a-z]+)(\s)(\d+\.\d+)", i, flags=re.IGNORECASE)
        # Parser2 = re.search(r"(BUY|SELL)([at@\s][\d+\.\d+])", i,  flags=re.IGNORECASE)
        print("parser", parser)
        if bool(parser) == True:
            print("printing parsers", parser)
            parser_span = parser.span()
            epstring = parser.string[parser_span[0]:parser_span[1]]
            ep_parse = re.findall(r'\d+\.\d+', epstring, flags=re.IGNORECASE)
            for ep in ep_parse:
                entry_price.append(float(ep))
    return sorted(entry_price)


# p = parser.groups()
# print("printing p", p)
# break


#     parser = re.search("^(BUY|SELL)\s([A-Z]*)\s[\(@at\s]*([0-9]*[.,][0-9]*)[\).]", i)

#     print("Printing parser",parser)
# x = re.findall(r'\d+\.\d+', example4)
# print(x)

# x = extractEP(rsignal)
# print("The entry price", x)

def cleanOrderData(rawsignal):
    rsignal = rawsignal.split("\n")
    response = {}
    symbol = extractSymbol(rsignal)
    side = extractSide(rsignal)
    tps = extractTps(rsignal)
    sls = extractSls(rsignal)
    eps = extractEP(rsignal)

    response.update({"symbol":symbol, "side":side})
    for tp in range(len(tps)):
        response.update({"takeProfit{0}".format(tp+1):tps[tp]})

    for sl in range(len(sls)):
        response.update({"stopLoss{0}".format(sl+1):sls[sl]})

    for ep in range(len(eps)):
        if len(eps)==1:
            response.update({"EntryPrice":eps[ep]})
        else:
            response.update({"EntryPrice{0}".format(ep+1):eps[ep]})

    return response
   


    