import requests
import sys
import csv

munis = ('CPT', 'JHB', 'TSH', 'BUF', 'MAN', 'NMA', 'DC40', 'FS183', 'NW373', 'EC141', 'NC094', 'DC43', 'KZN236', 'KZN265', 'NC091', 'NC078', 'KZN254', 'KZN285', 'LIM341', 'MP303', 'KZN244', 'WC014', 'MP305', 'NC071', 'KZN241', 'LIM471', 'WC041', 'NW384', 'EC157', 'LIM333', 'DC4', 'LIM362', 'DC10', 'KZN214', 'MP304', 'WC022', 'DC13', 'FS204', 'NW404', 'NW397', 'WC033', 'DC44', 'EC109', 'KZN432', 'FS195', 'WC023', 'EC106', 'FS196', 'GT423', 'MP302', 'DC23', 'LIM355', 'FS184', 'FS162', 'KZN272', 'LIM472', 'FS205', 'EC131', 'WC047', 'EC134', 'KZN282', 'DC42', 'WC025', 'EC104', 'DC21', 'EC441', 'DC6', 'LIM351', 'NC067', 'KZN224', 'NC084', 'NC064', 'EC136', 'NW371', 'DC22', 'LIM342', 'LIM366', 'DC38', 'MP316', 'MP312', 'DC25', 'KZN234', 'FS193', 'LIM331', 'KZN225', 'DC45', 'EC105', 'WC051', 'DC19', 'NC075', 'KZN261', 'LIM474', 'WC031', 'MP311', 'EC128', 'EC137', 'FS164', 'KZN222', 'FS201', 'KZN215', 'DC2', 'KZN253', 'LIM352', 'MP323', 'DC37', 'MP314', 'NW393', 'WC052', 'KZN274', 'FS192', 'KZN233', 'KZN433', 'NW372', 'WC043', 'EC124', 'NC077', 'KZN283', 'DC15', 'GT484', 'EC154', 'MP321', 'WC032', 'KZN252', 'LIM332', 'DC24', 'MP313', 'DC27', 'EC103', 'KZN431', 'LIM364', 'NW402', 'GT421', 'WC048', 'EKU', 'NC061', 'LIM473', 'DC39', 'NC065', 'KZN263', 'EC102', 'NC452', 'WC012', 'GT422', 'DC32', 'EC156', 'NC451', 'EC132', 'NC083', 'NW374', 'NC074', 'FS163', 'GT482', 'NW403', 'NC073', 'LIM334', 'DC18', 'LIM367', 'KZN223', 'KZN266', 'KZN275', 'DC36', 'LIM361', 'KZN284', 'NC072', 'KZN262', 'EC138', 'FS194', 'GT483', 'FS182', 'NC453', 'KZN221', 'EC127', 'EC126', 'DC5', 'KZN291', 'DC31', 'NC076', 'NC093', 'DC26', 'EC108', 'KZN293', 'MP322', 'NW385', 'WC013', 'NW375', 'EC101', 'EC133', 'NW381', 'NW394', 'DC29', 'NW382', 'NC081', 'NW401', 'KZN435', 'EC442', 'EC144', 'NC085', 'KZN281', 'DC1', 'MP315', 'DC8', 'KZN434', 'KZN211', 'WC015', 'LIM353', 'DC47', 'KZN226', 'KZN216', 'KZN232', 'NC066', 'NW396', 'MP325', 'KZN212', 'KZN242', 'KZN227', 'KZN292', 'MP301', 'EC444', 'EC122', 'LIM475', 'FS185', 'FS161', 'KZN271', 'EC121', 'EC155', 'DC7', 'EC153', 'KZN213', 'MP324', 'EC143', 'NW392', 'FS181', 'GT481', 'EC123', 'DC28', 'FS191', 'MP307', 'WC024', 'WC042', 'KZN273', 'NC062', 'DC34', 'LIM335', 'WC034', 'NW383', 'EC443', 'EC142', 'FS203', 'NC092', 'DC14', 'WC011', 'DC30', 'EC107', 'WC044', 'LIM343', 'LIM344', 'ETH', 'KZN235', 'KZN286', 'WC045', 'EC135', 'MP306', 'WC053', 'DC3', 'LIM354', 'DC48', 'NC086', 'DC35', 'NC082', 'DC16', 'DC20', 'LIM365', 'DC9', 'DC33', 'DC12', 'KZN245', 'KZN294', 'WC026')

periods = (
    (2015, 'AUDA'),
    (2015, 'ORGB'),
    (2014, 'AUDA'),
    (2014, 'ORGB'),
    (2013, 'AUDA'),
    (2013, 'ORGB'),
    (2012, 'AUDA'),
    (2012, 'ORGB'),
)

fields = ['cube', 'demarcation_code', 'financial_year', 'amount_type', 'has_data']

cubes = [
    'repmaint',
    'bsheet',
    'incexp',
    'capital',
    'cflow',
]

writer = csv.DictWriter(sys.stdout, fields)
writer.writeheader()

for cube in cubes:
    for (year, type) in periods:
        for muni in munis:
            cuts = [
                "demarcation:\"%s\"" % muni,
                "financial_year_end:%s" % year,
                "financial_period:%s" % year,
                "period_length:\"year\"",
                "amount_type:\"%s\"" % type,
            ]
            cutstr = '|'.join(cuts)
            params = {
                'cut': cutstr
            }
            r = requests.get(
                "http://172.17.0.2:8000/api/cubes/%s/facts" % cube,
                params=params
            )
            r.raise_for_status()
            result = r.json()
            has_data = result['total_fact_count'] > 0
            row = {
                'cube': cube,
                'demarcation_code': muni,
                'financial_year': year,
                'amount_type': type,
                'has_data': has_data,
            }
            writer.writerow(row)
