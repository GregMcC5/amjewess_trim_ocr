import metadata_utils as mu
import xml.etree.ElementTree as ET
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def chop(divs):
    for idx,div in enumerate(divs):
            if div != divs[-1]:
            #if the last page of the current article div matches the first page of the next article div...  
                if [x for x in div.iter('PB')][-1].attrib["REF"] == [x for x in divs[idx+1].iter('PB')][0].attrib["REF"]:

                    title = [x for x in divs[idx+1].iter("TITLE")][0].text
                    line_break1 = None
                    line_break2 = None

                    #--Find Breaks--

                    #-Line Break 1 (for Current DIV)
                    for i, line in enumerate([x for x in divs[idx].iter('PB')][-1].tail.splitlines()):
                        if i not in (0,1):
                            if title in line:
                                line_break1 = i
                                print('found break')
                                break
                    if not line_break1:
                        line_break1 = process.extractOne(title, [line for line in list(divs[idx].iter("PB"))[-1].tail.splitlines()[2:]])[0]
                        line_break1 = list(list(divs[idx].iter("PB"))[-1].tail.splitlines()).index(line_break1)
                        print("processed line break", line_break1)
                    if not line_break1:
                        print("more issues")

                    #-Line Break 2 (for Next DIV)
                    for i, line in enumerate([x for x in divs[idx+1].iter('PB')][0].tail.splitlines()):
                        if i not in (0,1):
                            if title in line:
                                line_break2 = i
                                print('found break')
                                break
                    if not line_break2:
                        line_break2 = process.extractOne(title, [line for line in list(divs[idx+1].iter("PB"))[0].tail.splitlines()[2:]])[0]
                        line_break2 = list(list(divs[idx+1].iter("PB"))[0].tail.splitlines()).index(line_break2)
                        print("processed line break", line_break2)
                    if not line_break2:
                        print("more issues")

                    #--Trim from Breaks--

                    #-Trimming Page Text for Current DIV
                    new_pg = ET.Element("P")
                    new_pb = ET.Element("PB")
                    for key,val in [x for x in div.iter('PB')][-1].attrib.items():
                        new_pb.attrib[key] = val
                    new_pb.tail = "  \n\n" + "\n".join([x for x in div.iter('PB')][-1].tail.splitlines()[:line_break1]+["\n","\n"])
                    new_pg.append(new_pb)
                    divs[idx][-1] = new_pg

                    #-Trimming Page Text for Next DIV
                    new_pg2 = ET.Element("P")
                    new_pb2 = ET.Element("PB")
                    for key,val in [x for x in divs[idx+1].iter("PB")][0].attrib.items():
                        new_pb2.attrib[key] = val
                    new_pb2.tail = "  \n\n" + "\n".join([x for x in divs[idx+1].iter("PB")][0].tail.splitlines()[line_break2:]+["\n","\n"])
                    new_pg2.append(new_pb2)
                    divs[idx+1][1] = new_pg2
    return divs


def main():
    #Load XML
    tree = ET.parse(f"amjewess.xml")
    root = tree.getroot()

    for volume in root.iter("DLPSTEXTCLASS"):

        #Chop OCR
        divs = [x for x in volume.iter("DIV1")]
        divs = chop(divs)

        #Replace Current Body with Chopped OCRs
        text = volume.find("./TEXT")
        body = volume.find("./TEXT/BODY")
        text.remove(body)
        new_body = ET.Element("BODY")
        for div1 in divs:
            new_body.append(div1)
        text.append(new_body)

    #Write it
    tree.write(f'amjewess_chopped.xml')
    print("wrote amjewess_chopped.xml")

if __name__ == "__main__":
    main()
    print("done")