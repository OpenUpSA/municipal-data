--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

DROP INDEX IF EXISTS public.scorecard_geography_url_idx;
DROP INDEX IF EXISTS public.scorecard_geography_street_address_4_idx;
DROP INDEX IF EXISTS public.scorecard_geography_street_address_3_idx;
DROP INDEX IF EXISTS public.scorecard_geography_street_address_2_idx;
DROP INDEX IF EXISTS public.scorecard_geography_street_address_1_idx;
DROP INDEX IF EXISTS public.scorecard_geography_province_name_idx;
DROP INDEX IF EXISTS public.scorecard_geography_province_code_idx;
DROP INDEX IF EXISTS public.scorecard_geography_postal_address_3_idx;
DROP INDEX IF EXISTS public.scorecard_geography_postal_address_2_idx;
DROP INDEX IF EXISTS public.scorecard_geography_postal_address_1_idx;
DROP INDEX IF EXISTS public.scorecard_geography_phone_number_idx;
DROP INDEX IF EXISTS public.scorecard_geography_parent_code_idx;
DROP INDEX IF EXISTS public.scorecard_geography_name_idx;
DROP INDEX IF EXISTS public.scorecard_geography_name_52e408f6_like;
DROP INDEX IF EXISTS public.scorecard_geography_long_name_idx;
DROP INDEX IF EXISTS public.scorecard_geography_long_name_d5fe0964_like;
DROP INDEX IF EXISTS public.scorecard_geography_geo_code_idx;
DROP INDEX IF EXISTS public.scorecard_geography_fax_number_idx;
DROP INDEX IF EXISTS public.scorecard_geography_dimension_municipality_idx;
DROP INDEX IF EXISTS public.scorecard_geography_dimension_demarcation_idx;
DROP INDEX IF EXISTS public.scorecard_geography_category_idx;
DROP INDEX IF EXISTS public.scorecard_geography_b068931c;
DROP INDEX IF EXISTS public.scorecard_geography_2fc6351a;
ALTER TABLE IF EXISTS ONLY public.scorecard_geography DROP CONSTRAINT IF EXISTS scorecard_geography_unique_geo_code;
ALTER TABLE IF EXISTS ONLY public.scorecard_geography DROP CONSTRAINT IF EXISTS scorecard_geography_pkey;
ALTER TABLE IF EXISTS ONLY public.scorecard_geography DROP CONSTRAINT IF EXISTS scorecard_geography_geo_level_1b28c178_uniq;
ALTER TABLE IF EXISTS public.scorecard_geography ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.scorecard_geography_id_seq;
DROP TABLE IF EXISTS public.scorecard_geography;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: scorecard_geography; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE scorecard_geography (
    id integer NOT NULL,
    geo_level character varying(15) NOT NULL,
    geo_code character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    long_name character varying(100),
    square_kms double precision,
    parent_level character varying(15),
    parent_code character varying(10),
    province_name character varying(100) NOT NULL,
    province_code character varying(5) NOT NULL,
    category character varying(2) NOT NULL,
    postal_address_1 text,
    postal_address_2 text,
    postal_address_3 text,
    street_address_1 text,
    street_address_2 text,
    street_address_4 text,
    phone_number text,
    fax_number text,
    url text,
    street_address_3 text,
    miif_category text,
    population integer
);


--
-- Name: scorecard_geography_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE scorecard_geography_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: scorecard_geography_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE scorecard_geography_id_seq OWNED BY scorecard_geography.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY scorecard_geography ALTER COLUMN id SET DEFAULT nextval('scorecard_geography_id_seq'::regclass);


--
-- Data for Name: scorecard_geography; Type: TABLE DATA; Schema: public; Owner: -
--

COPY scorecard_geography (id, geo_level, geo_code, name, long_name, square_kms, parent_level, parent_code, province_name, province_code, category, postal_address_1, postal_address_2, postal_address_3, street_address_1, street_address_2, street_address_4, phone_number, fax_number, url, street_address_3, miif_category, population) FROM stdin;
310	municipality	EC139	Enoch Mgijima	Enoch Mgijima, Eastern Cape	13595.2259765481504	district	DC13	Eastern Cape	EC	B	Private Bag X 7111	Queenstown	5320	Town Hall	70 Cathcart Road	5320	045 807 2606	045 807 2637	http://www.lukhanji.co.za	Queenstown	B2	\N
309	municipality	EC129	Raymond Mhlaba	Raymond Mhlaba, Eastern Cape	6360.93523551468024	district	DC12	Eastern Cape	EC	B	36	Fort Beaufort	5720	8	Somerste Street	5720	046 645 7400	046 645 2562	http://www.raymondmhlaba.gov.za	Fort Beaufort	B3	\N
311	municipality	EC145	Walter Sisulu	Walter Sisulu, Eastern Cape	13280.9772392252398	district	DC14	Eastern Cape	EC	B	P O BOX 13	BURGERSDORP	9744	\N	01 Jan Greyling Street	9744	051 653 1777	051 653 0056	\N	Burgersdorp	B3	\N
312	municipality	GT485	Rand West City	Rand West City, Gauteng	1116.77439619296001	district	DC48	Gauteng	GT	B	218	RANDFONTEIN	1760	Rand West City	Cnr Pollock & Sutherland Streets	1760	011 411 0000	011 693 1736	http://www.randwestcity.gov.za	Randfontein	B2	\N
314	municipality	KZN238	Alfred Duma	Alfred Duma, KwaZulu-Natal	3769.87215634065979	district	DC23	KwaZulu-Natal	KZN	B	PO BOX 29	Ladysmith	3370	Lister Clarence Building	221 Murchison Street	3370	036 637 2231	036 631 1400	\N	Ladysmith	B2	\N
316	municipality	KZN436	Dr Nkosazana Dlamini Zuma	Dr Nkosazana Dlamini Zuma, KwaZulu-Natal	3606.10194712296015	district	DC43	KwaZulu-Natal	KZN	B	P O BOX 62	CREIGHTON	3263	Municipal Office	Main Strees	3263	039 833 1038	039 833 1179	http://www.ndz.gov.za	Creighton	B3	\N
313	municipality	KZN237	Inkosi Langalibalele	Inkosi Langalibalele, KwaZulu-Natal	3403.27981805951003	district	DC23	KwaZulu-Natal	KZN	B	15	ESTCOURT	3310	CIVIC BUILDING	VICTORIA STREET	3310	036 342 7800	036 352 5829	http://www.umtshezi.co.za	ESTCOURT	B3	\N
315	municipality	KZN276	Big Five Hlabisa	Big Five Hlabisa, KwaZulu-Natal	3471.40416055176001	district	DC27	KwaZulu-Natal	KZN	B	387	Hlabisa	3937	Lot 808	Off Masson Street	3937	035 838 8500	035 838 1015	http://www.big5hlabisa.gov.za	Hlabisa	B3	\N
319	municipality	LIM476	Greater Tubatse/Fetakgomo	Greater Tubatse/Fetakgomo, Limpopo	5705.73268331088002	district	DC47	Limpopo	LIM	B	P O BOX 260	BURGERSFORD	1150	No 1	Kastania	1150	013 231 1000	\N	\N	Burgersford	B4	\N
317	municipality	LIM345	Makhado-Thulamela	Makhado-Thulamela, Limpopo	5015.40777477557003	district	DC34	Limpopo	LIM	B	Private Bag X 9271	Malamulele	0982	Buiding DCO	225 Hospital	0982	015 851 0110	015 851 0097	http://www.lim345.gov.za	Malamulele	B4	\N
318	municipality	LIM368	Modimolle/Mookgophong	Modimolle/Mookgophong, Limpopo	10389.3492549759194	district	DC36	Limpopo	LIM	B	PRIVATE BAG X1008	MODIMOLLE	0510	O R Tambo Square	Harry Gwala Street	0510	014 718 2000	014 717 4077	\N	Modimolle	B3	\N
144	municipality	LIM343	Thulamela	Thulamela, Limpopo	2648.16848366380009	district	DC34	Limpopo	LIM	B	PRIVATE BAG X5066	THOHOYANDOU	0950	Old Agriven Building Ardc	Thohoyandou	\N	015 962 7500	015 962 4020	http://www.thulamela.gov.za	0950	B4	618462
322	municipality	NW405	Ventersdorp/Tlokwe	Ventersdorp/Tlokwe, North West	6409.58403342761994	district	DC40	North West	NW	B	X 13	Potchefstroom	2520	Dan Tloome	Wolmaraans	2520	018 299 5111	\N	\N	Potchefstroom	B1	\N
321	municipality	NC087	Dawid Kruiper	Dawid Kruiper, Northern Cape	44306.5209873748972	district	DC8	Northern Cape	NC	B	PRIVATE BAG X 6003	UPINGTON	8800	Civic Centre	2 Mark Street	8801	054 338 7000	054 338 7350	\N	Upington	B2	\N
320	municipality	MP326	Mbombela	Mbombela, Mpumalanga	7155.80187952501001	district	DC32	Mpumalanga	MP	B	45	MBOMBELA	1200	Civic Centre	1 Nel Street	1200	013 759 9111	013 759 2070	http://www.mbombela.gov.za	Mbombela	B1	\N
155	municipality	EC101	Dr Beyers Naude	Dr Beyers Naude, Eastern Cape	28668.4905107623417	district	DC10	Eastern Cape	EC	B	P O BOX 71	GRAAFF- REINET	6280	The Town Hall	Church Square	6280	049 807 5700	049 892 6137	http://www.camdeboo.gov.za	Graaff-Reinet	B3	50993
56	municipality	EC102	Blue Crane Route	Blue Crane Route, Eastern Cape	11074.9259919529195	district	DC10	Eastern Cape	EC	B	P O BOX 21	SOMERSET EAST	5850	Town Hall	67 Nojoli Street	5850	042 243 6400	042 243 2250	http://www.bcrm.gov.za	Somerset East	B3	36002
57	municipality	EC103	Ikwezi	Ikwezi, Eastern Cape	4562.72999999999956	district	DC10	Eastern Cape	EC	B	P.O BOX 12	JANSENVILLE	6265	34 Main Street	Jansenville	\N	049 836 0021	049 836 0105	http://www.ikwezimunicipality.co.za	6265	B3	10537
58	municipality	EC104	Makana	Makana, Eastern Cape	4377.56326434091989	district	DC10	Eastern Cape	EC	B	P O BOX 176	GRAHAMSTOWN	6140	City Hall	86 High Street	6139	046 603 6111	046 622 9488	http://www.makana.gov.za	Grahamstown	B2	80390
156	municipality	EC105	Ndlambe	Ndlambe, Eastern Cape	1841.37914226551993	district	DC10	Eastern Cape	EC	B	P.O BOX 13	PORT ALFRED	6170	Civic Centre	Causeway Road	6170	046 604 5500	046 624 2727	http://www.ndlambe.co.za	Port Alfred	B3	61176
59	municipality	EC106	Sundays River Valley	Sundays River Valley, Eastern Cape	5997.37604280511005	district	DC10	Eastern Cape	EC	B	P O BOX 47	KIRKWOOD	6120	30 Middle Street	Kirkwood	\N	042 230 7700	042 230 1799	http://www.srvm.co.za	6120	B3	54504
60	municipality	EC107	Baviaans	Baviaans, Eastern Cape	11668.2999999999993	district	DC10	Eastern Cape	EC	B	P O BOX 15	WILLOWMORE	6445	Baviaans Municipality	42 Wehmeyer Street	6445	044 923 1004	044 923 1122	http://www.baviaans.co.za	Willowmore	B3	17761
61	municipality	EC108	Kouga	Kouga, Eastern Cape	2671.29628107146982	district	DC10	Eastern Cape	EC	B	P O BOX 21	JEFFREYS BAY	6330	Municipal Buildings	33 Da Gama Road	6330	042 200 2200	042 200 8606	http://www.kougamunicipality.gov.za	Jeffreys Bay	B3	98558
62	municipality	EC109	Kou-Kamma	Kou-Kamma, Eastern Cape	3642.96182473210001	district	DC10	Eastern Cape	EC	B	PRIVATE BAG X0011	KAREEDOUW	6400	Municipal Building	5 Keet Street	6400	042 288 0303 / 7200	042 288 0797	http://www.koukammamunicipality.co.za	Kareedouw	B3	40663
63	municipality	EC121	Mbhashe	Mbhashe, Eastern Cape	3304.77899008598979	district	DC12	Eastern Cape	EC	B	PO BOX 25	DUTYWA	5000	Mbhashe Local Municipality Offices	Idutywa	5000	047 489 5800	047 489 1137	http://www.mbhashemun.gov.za	DUTYWA	B4	254909
157	municipality	EC122	Mnquma	Mnquma, Eastern Cape	3139.27509706805995	district	DC12	Eastern Cape	EC	B	P.O.BOX 36	BUTTERWORTH	4960	Ngumbela Building	Corner King and Mthatha Street	4960	047 401 2400	047 491 0195	http://www.mnquma.gov.za	Butterworth	B4	252390
64	municipality	EC123	Great Kei	Great Kei, Eastern Cape	1700.85919255661997	district	DC12	Eastern Cape	EC	B	PRIVATE BAG X2	KOMGA	4950	Council Buildings	17 Main Street	4950	043 831 5700	043 831 1306	http://www.greatkeilm.gov.za	Komga	B3	38991
65	municipality	EC124	Amahlathi	Amahlathi, Eastern Cape	4508.22438319672983	district	DC12	Eastern Cape	EC	B	Private Bag X4002	Stutterheim	4930	Amahlathi Municipality	12 Maclean street	4939	043 683 5000	043 683 1070	http://www.amahlathi.gov.za	Stutterheim	B3	122778
66	municipality	EC126	Ngqushwa	Ngqushwa, Eastern Cape	2115.67379920125995	district	DC12	Eastern Cape	EC	B	PO BOX 539	PEDDIE	5640	Ngqushwa Municipality	Erf 313	5640	040 673 3095	040 673 3771	http://www.ngqushwamun.gov.za	Peddie	B4	72190
67	municipality	EC127	Nkonkobe	Nkonkobe, Eastern Cape	3626.17999999999984	district	DC12	Eastern Cape	EC	B	PO BOX 36	FORT BEAUFORT	5720	\N	8 Somerset Street	5720	046 645 7400	046 645 1619	http://www.nkonkobe.co.za	Fort Beaufort	B3	127115
158	municipality	EC128	Nxuba	Nxuba, Eastern Cape	2731.92000000000007	district	DC12	Eastern Cape	EC	B	PRIVATE BAG X350	ADELAIDE	5760	Municipal Buildings	Market Square	5760	046 684 0034	046 684 1931	http://www.nxuba.co.za	Adelaide	B3	24264
68	municipality	EC131	Inxuba Yethemba	Inxuba Yethemba, Eastern Cape	11672.12804744598	district	DC13	Eastern Cape	EC	B	P O BOX 24	CRADOCK	5880	Civic Centre	J A Calata Street	5880	048 801 5000	048 881 1421	\N	Cradock	B3	65560
69	municipality	EC132	Tsolwana	Tsolwana, Eastern Cape	6086.81999999999971	district	DC13	Eastern Cape	EC	B	P O BOX 12	TARKASTAD	5370	Municipal Offices	12 Murray Street	5370	045 846 0033/0077/0270	045 846 0025 /0408	http://www.tsolwana.co.za	Tarkastad	B3	33281
70	municipality	EC133	Inkwanca	Inkwanca, Eastern Cape	3584.23999999999978	district	DC13	Eastern Cape	EC	B	P O BOX 1	MOLTENO	5500	Inkwanca Municipality	39 Smith Street	5500	045 967 0021	045 967 0467	http://www.ecprov.gov.za/Inkwancalm	Molteno	B3	21971
71	municipality	EC134	Lukanji	Lukanji, Eastern Cape	3812.86000000000013	district	DC13	Eastern Cape	EC	B	PRIVATE BAG X 7111	QUEENSTOWN	5320	Town Hall Building	5-7 Cathcart Road	5320	045 807 2000	045 807 2733	http://www.lukhanji.co.za	Queenstown	B2	190723
159	municipality	EC135	Intsika Yethu	Intsika Yethu, Eastern Cape	2875.47401411339979	district	DC13	Eastern Cape	EC	B	P O BOX 1251	COFIMVABA	5380	Main Building	201 Main Street	5380	047 874 0704	047 874 0010	http://www.intsikayethu.gov.za	Cofimvaba	B4	145372
72	municipality	EC136	Emalahleni	Emalahleni, Eastern Cape	3487.01503713838019	district	DC13	Eastern Cape	EC	B	PRIVATE BAG X1161	LADY FRERE	5410	37	Indwe Road	5410	047 878 2000	047 878 0112	http://www.emalahlenilm.gov.za	LADY FRERE	B4	119460
73	municipality	EC137	Engcobo	Engcobo, Eastern Cape	2485.79582750784994	district	DC13	Eastern Cape	EC	B	P O BOX 24	ENGCOBO	5050	Town Hall	58 Union Street	5050	047 548 1221	047 548 1078	\N	Engcobo	B4	155513
74	municipality	EC138	Sakhisizwe	Sakhisizwe, Eastern Cape	2319.54599329363009	district	DC13	Eastern Cape	EC	B	P.O. Box.26	Cala	5460	Old Convent	5557 Umtata Road	5455	047 877 5200	047 877 0000	http://www.sakhisizwe.gov.za	Cala	B3	63582
75	municipality	EC141	Elundini	Elundini, Eastern Cape	5023.52411180956005	district	DC14	Eastern Cape	EC	B	PO BOX 1	MACLEAR	5480	Elundini Municipality	1 Seller Street	5480	045 932 8100	045 932 1094	http://www.elundini.gov.za	Maclear	B4	138141
76	municipality	EC142	Senqu	Senqu, Eastern Cape	7336.39162129922988	district	DC14	Eastern Cape	EC	B	Private Bag X 03	LADY GREY	9755	\N	18 Murray Street	9755	051 603 1300	051 603 0445	http://www.senqu.gov.za	Lady Grey	B4	134150
77	municipality	EC143	Maletswai	Maletswai, Eastern Cape	4357.64999999999964	district	DC14	Eastern Cape	EC	B	PRIVATE BAG X 1011	ALIWAL NORTH	9750	\N	C/O Barkly And Smith Street	9750	051 633 2441	051 634 1307	http://www.maletswai.gov.za	Aliwal North	B3	43800
160	municipality	EC144	Gariep	Gariep, Eastern Cape	8911.05999999999949	district	DC14	Eastern Cape	EC	B	P O BOX 13	BURGERSDORP	9744	\N	1 Jan Greyling Street	9744	051 653 1777	051 653 0056	http://www.gariep.gov.za	Burgersdorp	B3	33677
78	municipality	EC153	Ngquza Hill	Ngquza Hill, Eastern Cape	2478.99109848572016	district	DC15	Eastern Cape	EC	B	P O BOX 14	FLAGSTAFF	4810	Ingquza Hill Local Municipality	135 Main Street	4810	039 252 0131/0090/0089	039 252 0699	http://www.ihlm.gov.za	Flagstaff	B4	278481
51	municipality	EC154	Port St Johns	Port St Johns, Eastern Cape	1292.24767922709998	district	DC15	Eastern Cape	EC	B	P.O BOX 2	PORT ST JOHN'S	5120	Town Hall	Erf 257 Main Street	5120	047 564 1208	047 564 1206	http://www.psjlm.co.za	Port St John'S	B4	156136
52	municipality	EC155	Nyandeni	Nyandeni, Eastern Cape	2475.9871262039801	district	DC15	Eastern Cape	EC	B	PRIVATE BAG X504	LIBODE	5160	Municipal House	89 B Nomandela Drive	5160	047 555 5000	047 555 0202	http://www.nyandenilm.gov.za	Libode	B4	290390
79	municipality	EC156	Mhlontlo	Mhlontlo, Eastern Cape	2882.77633281081989	district	DC15	Eastern Cape	EC	B	PO BOX 31	QUMBU	5180	97 Church Street	Qumbu	\N	047 553 7000	047 553 0153/89	http://www.mhlontlolm.gov.za	5180	B4	188226
161	municipality	EC157	King Sabata Dalindyebo	King Sabata Dalindyebo, Eastern Cape	3021.23247260769995	district	DC15	Eastern Cape	EC	B	P O BOX 45	MTHATHA	5099	Munitata Building	Cnr Sutherland & Yorke Road	5099	047 501 4003	047 531 2861	http://www.ksd.org.za	Mthatha	B2	451710
80	municipality	EC441	Matatiele	Matatiele, Eastern Cape	4356.90957791715027	district	DC44	Eastern Cape	EC	B	P.O. BOX 35	MATATIELE	4730	\N	102 Main Street	4730	039 737 8100	039 737 3611	http://www.matatiele.gov.za	Matatiele	B3	203843
45	municipality	EC442	Umzimvubu	Umzimvubu, Eastern Cape	2581.39760435336984	district	DC44	Eastern Cape	EC	B	PRIVATE BAG X9020	MOUNT FRERE	5090	813 Main Street	Mount Frere	\N	039 255 0166	039 255 0167	http://www.umzimvubu.org.za	5090	B4	191620
46	municipality	EC443	Mbizana	Mbizana, Eastern Cape	2417.74140892600008	district	DC44	Eastern Cape	EC	B	P O BOX 12	MBIZANA	4800	Municipal Offices	51 Main Street	4800	039 251 0230	039 251 0917	http://www.mbizana.gov.za	Bizana	B4	281905
47	municipality	EC444	Ntabankulu	Ntabankulu, Eastern Cape	1385.79787907603009	district	DC44	Eastern Cape	EC	B	P.O. BOX 234	NTABANKULU	5130	Municipal Buildings	Erf 85 Main Stret	5130	039 258 0056	039 258 0003	\N	Ntabankulu	B4	123976
154	municipality	BUF	Buffalo City	Buffalo City, Eastern Cape	2751.69154949281983	province	EC	Eastern Cape	EC	A	P O BOX 134	EAST LONDON	5200	Trust Bank Centre	C/O Oxford & North Street	5200	043 705 2000	043 743 8568	http://www.buffalocity.gov.za	East London	A	755200
162	municipality	NMA	Nelson Mandela Bay	Nelson Mandela Bay, Eastern Cape	1957.60149955772999	province	EC	Eastern Cape	EC	A	116	Port Elizabeth	6000	City Hall	Govan Mbeki	6000	041 506 1911	041 506 1444	http://www.mandelametro.gov.za	Port Elizabeth	A	1152115
48	municipality	FS161	Letsemeng	Letsemeng, Free State	9840.83445639417914	district	DC16	Free State	FS	B	PRIVATE BAG X3	KOFFIEFONTEIN	9986	Municipal Offices	Groottrekstraat 7	9986	053 205 9200	053 205 0144	http://www.letsemeng.gov.za	Koffiefontein	B3	38628
49	municipality	FS162	Kopanong	Kopanong, Free State	15663.2377684441508	district	DC16	Free State	FS	B	P O BOX 23	TROMPSBURG	9913	Xhariep District Municipality Building	20 Louw Street	9913	051 713 9200	051 713 0292	http://www.kopanong.gov.za	Trompsburg	B3	49171
50	municipality	FS163	Mohokare	Mohokare, Free State	8785.27708159997019	district	DC16	Free State	FS	B	P.O. BOX 20	ZASTRON	9950	Municipal Building	20 Hoofd Street	9950	051 673 9600	051 673 1550	http://www.mohokare.gov.za	Zastron	B3	34146
163	municipality	FS164	Naledi	Naledi, Free State	3424.05999999999995	district	DC16	Free State	FS	B	PRIVATE BAG X 1	DEWETSDORP	9940	Brand Street	Dewetsdorp	\N	051 541 0012	051 541 0556	\N	9940	B3	24314
53	municipality	FS181	Masilonyana	Masilonyana, Free State	6627.10197414601043	district	DC18	Free State	FS	B	P O BOX 8	THEUNISSEN	9410	Masilonyana Local Municipality	24 Le Roux Street	9410	057 733 0106	057 733 2217	http://www.masilonyana.local.gov.za	Theunissen	B3	63334
54	municipality	FS182	Tokologo	Tokologo, Free State	9339.22797611825081	district	DC18	Free State	FS	B	PRIVATE BAG X46	BOSHOF	8340	Municipal Offices	Voortrekker Street	8340	053 541 0014	053 541 0360	http://tokologo.org.za/	Boshof	B3	28986
55	municipality	FS183	Tswelopele	Tswelopele, Free State	6533.94198457039965	district	DC18	Free State	FS	B	P O BOX 3	BULTFONTEIN	9670	Civic Centre	Bosman Street	9670	051 853 1111	051 853 1332	http://www.tswelopele.gov.za	Bultfontein	B3	47625
81	municipality	FS184	Matjhabeng	Matjhabeng, Free State	5699.05622231179041	district	DC18	Free State	FS	B	P O BOX 708	Welkom	9459	Civic Building	Cnr Ryk & Heeren street	9459	057 391 3911	057 352 1448	http://www.matjhabeng.fs.gov.za	Welkom	B1	406461
82	municipality	FS185	Nala	Nala, Free State	4135.39116444990032	district	DC18	Free State	FS	B	PRIVATE BAG X15	BOTHAVILLE	9660	Municipal Building	8 Preller Street	9660	056 514 9200	056 515 3922	http://www.nala.org.za	Bothaville	B3	81220
164	municipality	FS191	Setsoto	Setsoto, Free State	5439.04331454585008	district	DC19	Free State	FS	B	P O BOX 116	FICKSBURG	9730	Municipal Buildings	27 Voortrekker Street	9730	051 933 9300	051 933 9343	http://www.setsoto.co.za	Ficksburg	B3	112597
83	municipality	FS192	Dihlabeng	Dihlabeng, Free State	4874.58134801693996	district	DC19	Free State	FS	B	P O BOX 551	BETHLEHEM	9700	Dihlabeng Hq	9 Muller Street East	9701	058 303 5732	058 303 5513	http://www.dihlabeng.co.za	Bethlehem	B2	128704
84	municipality	FS193	Nketoana	Nketoana, Free State	5619.73038704757982	district	DC19	Free State	FS	B	P O BOX 26	REITZ	9810	Municipal Building	Cnr Church & Voortrekker Street	9810	058 863 2811	058 863 2523	http://www.nketoanafs.gov.za	Reitz	B3	60324
85	municipality	FS194	Maluti a Phofung	Maluti a Phofung, Free State	4344.05349452028986	district	DC19	Free State	FS	B	P/ BAG X805	WITSIESHOEK	9870	Setsing Bus Centre	Cnr Motloung & Moremoholo	9866	058 718 3700	058 718 3777	http://www.map.fs.gov.za	Phuthaditjhaba	B3	335784
86	municipality	FS195	Phumelela	Phumelela, Free State	8208.9667851127906	district	DC19	Free State	FS	B	PRIVATE BAG X5	VREDE	9835	Municipal Administrative Offices	52 Kuhn Street	9835	058 913 8323	058 913 2317	http://www.phumelelamun.co.za	Vrede	B3	47772
165	municipality	FS196	Mantsopa	Mantsopa, Free State	4296.16883523723027	district	DC19	Free State	FS	B	P O BOX 64	LADYBRAND	9745	Civic Centre	Joubert Street	9745	051 924 0654	051 924 0020	http://www.mantsopa.fs.gov.za	Ladybrand	B3	51056
87	municipality	FS201	Moqhaka	Moqhaka, Free State	7937.39629510744999	district	DC20	Free State	FS	B	P O BOX 302	KROONSTAD	9500	Municipal Offices	Hill Street	9500	056 216 9000	056 216 9122	\N	Kroonstad	B2	160532
88	municipality	FS203	Ngwathe	Ngwathe, Free State	7066.72503876613973	district	DC20	Free State	FS	B	P.O BOX 359	PARYS	9585	Municipal Building	Liebenberg Street	9585	056 816 2700	056 811 2046	http://www.ngwathe.fs.gov.za	Parys	B3	120520
89	municipality	FS204	Metsimaholo	Metsimaholo, Free State	1720.07039170892995	district	DC20	Free State	FS	B	P O BOX 60	SASOLBURG	1947	Civic Centre	Fichardt Street	1947	016 973 8301	016 976 2191	http://www.metsimaholo.gov.za	Sasolburg	B2	149108
90	municipality	FS205	Mafube	Mafube, Free State	3977.91300601796002	district	DC20	Free State	FS	B	P O BOX 2	FRANKFORT	9830	Mafube Local Municipality	64 JJ Hadebe Street	9830	058 813 1051	058 813 3072	http://www.mafubemunicipality.gov.za	Frankfort	B3	57876
166	municipality	MAN	Mangaung	Mangaung, Free State	9899.13857507013017	province	FS	Free State	FS	A	P O BOX 3704	BLOEMFONTEIN	9300	Bram Fischer Building	Cnr Nelson Mandela And Markgraaf Street	9301	051 405 8911	051 405 8108	http://www.mangaung.co.za	Bloemfontein	A	747431
91	municipality	GT421	Emfuleni	Emfuleni, Gauteng	967.619972499619962	district	DC42	Gauteng	GT	B	P O BOX 3	VANDERBIJLPARK	1900	C /O Klasie Havenga & Frikkie Meyer	Vanderbijlpark	\N	016 950 5102	016 950 5030	http://www.emfuleni.gov.za	1911	B1	721663
168	municipality	GT422	Midvaal	Midvaal, Gauteng	1725.55506590600999	district	DC42	Gauteng	GT	B	P O BOX 9	MEYERTON	1960	Municipal Buildings	Cnr Mitchel & Junius Street	1960	016 360 7400	016 360 7519	http://www.midvaal.gov.za	Meyerton	B2	95301
92	municipality	GT423	Lesedi	Lesedi, Gauteng	1487.09141075977004	district	DC42	Gauteng	GT	B	P O BOX 201	HEIDELBERG	1438	1 H F Verwoerd Street	C/O H F Verwoerd & Louw Streets	1441	016 330 0400	016 340 6458	http://www.lesedi.gov.za	Heidelberg	B3	99520
93	municipality	GT481	Mogale City	Mogale City, Gauteng	1344.72229091785994	district	DC48	Gauteng	GT	B	PO BOX 94	KRUGERSDORP	1740	The Civic Centre	Cnr Commissioner And Market Street	1740	011 951 2092	011 660 4043	http://www.mogalecity.gov.za	Krugersdorp	B1	362422
94	municipality	GT482	Randfontein	Randfontein, Gauteng	474.894000000000005	district	DC48	Gauteng	GT	B	P O BOX 218	RANDFONTEIN	1760	Civic Centre	C/O Sutherland & Pollock Streets	1759	011 411 0000	011 693 1394	http://www.randfontein.org.za	Randfontein	B2	149286
95	municipality	GT483	Westonaria	Westonaria, Gauteng	639.823999999999955	district	DC48	Gauteng	GT	B	P O BOX 19	WESTONARIA	1780	Civic Centre	C/O Neptunes & Saturnus Streets	1779	011 278 3140	011 753 4176	http://www.westonaria.gov.za	Westonoria	B2	111767
169	municipality	GT484	Merafong City	Merafong City, Gauteng	1633.52283066638006	district	DC48	Gauteng	GT	B	P O BOX 3	CARLETONVILLE	2500	Civic Centre	Halite Street	2500	018 788 9500	018 786 1105	http://www.merafong.co.za	Carltonville	B2	197520
167	municipality	EKU	Ekurhuleni	Ekurhuleni, Gauteng	1979.04473747871998	province	GT	Gauteng	GT	A	P/BAG X1069	GERMISTON	1400	Head Office	Cnr Cross And Rose Street	1401	011 999 0863	011 820 4311	http://www.ekurhuleni.gov.za	Germiston	A	3178470
170	municipality	JHB	City of Johannesburg	City of Johannesburg, Gauteng	1648.00938632176008	province	GT	Gauteng	GT	A	PO BOX 1049	JOHANNESBURG	2000	Metro Centre	158 Civic Boulevard Street	2000	011 358 3041	011 358 3140	http://www.joburg.org.za	Braamfontein	A	4434827
171	municipality	TSH	City of Tshwane	City of Tshwane, Gauteng	6310.21760217517021	province	GT	Gauteng	GT	A	P O BOX 6338	Pretoria	0001	Isivuno House	Cnr Lilian Ngoiyi & Madiba Street	0002	012 358 7911	012 358 1112	http://www.tshwane.gov.za	Pretoria	A	2921488
98	municipality	KZN213	Umzumbe	Umzumbe, KwaZulu-Natal	1222.18282016202011	district	DC21	KwaZulu-Natal	KZN	B	P.O BOX 561	HIBBERDENE	4220	561 Siphofu Road	Mathulini MPCC	4186	039 972 0005	039 972 0099	http://www.umzumbe.gov.za	Mthwalume	B4	160975
99	municipality	KZN214	uMuziwabantu	uMuziwabantu, KwaZulu-Natal	1090.56175145989005	district	DC21	KwaZulu-Natal	KZN	B	Private Bag X 1023	HARDING	4680	Municipal Offices	10 Murchison Street	4680	039 433 1205	039 433 1208	http://www.umuziwabantu.gov.za	Harding	B3	96556
100	municipality	KZN215	Ezingoleni	Ezingoleni, KwaZulu-Natal	648.07000000000005	district	DC21	KwaZulu-Natal	KZN	B	P O BOX 108	IZINGOLWENI	4260	Municipal Building	N2 Main Harding Road (Opp Taxi)	4260	039 534 1584 / 74 / 77	039 534 1585	http://www.ezingoleni.gov.za	Izingolweni	B4	52540
173	municipality	KZN216	Ray Nkonyeni	Ray Nkonyeni, KwaZulu-Natal	1488.52549396866993	district	DC21	KwaZulu-Natal	KZN	B	P O BOX 5	Port Shepstone	4240	Civic Centre	10 Connor Street	4240	039 688 2000	039 682 0327	http://www.rnm.gov.za	Port Shepstone	B2	256135
96	municipality	KZN211	Vulamehlo	Vulamehlo, KwaZulu-Natal	959.923999999999978	district	DC21	KwaZulu-Natal	KZN	B	P/BAG X5509	SCOTTBURGH	4180	P77 Dududu Main Road	Scottburgh Centre	\N	039 974 0450	039 974 0432	http://www.vulamehlo.org.za	4180	B4	77403
97	municipality	KZN212	Umdoni	Umdoni, KwaZulu-Natal	994.615916831559957	district	DC21	KwaZulu-Natal	KZN	B	P O BOX 19	SCOTTBURGH	4180	C/O Bram Fischer & Williamson Streets	Scottburgh	\N	039 976 1202	039 976 2044	http://www.umdoni.gov.za	4180	B2	78875
101	municipality	KZN221	uMshwathi	uMshwathi, KwaZulu-Natal	1867.90933503159999	district	DC22	KwaZulu-Natal	KZN	B	PRIVATE BAG X29	WARTBURG	3233	7 High Street	Wartburg	\N	033-5031035	033-5031635	\N	3233	B4	106374
102	municipality	KZN222	uMngeni	uMngeni, KwaZulu-Natal	1521.47535999155002	district	DC22	KwaZulu-Natal	KZN	B	P O BOX 5	HOWICK	3290	Municipal Buildings	C/O Sommer And Dicks Streets	3290	033 239 9200	033 330 4183	http://www.umngeni.gov.za	Howick	B2	92710
103	municipality	KZN223	Mpofana	Mpofana, KwaZulu-Natal	1758.86680855625991	district	DC22	KwaZulu-Natal	KZN	B	P O BOX 47	MOOI RIVER	3300	Mpofana Municipal Buildings	10 Claughton Terrace	3300	033 263 7700/1221	033 263 1127	http://www.mpofana.gov.za	Mooi River	B3	38103
104	municipality	KZN224	Impendle	Impendle, KwaZulu-Natal	1611.52967577454001	district	DC22	KwaZulu-Natal	KZN	B	P O BOX X512	IMPENDLE	3227	Impendle Municipality	21 Mafahleni Street	3227	033 996 0771	033 996 0852	http://www.impendle.gov.za	Impendle	B4	33105
105	municipality	KZN225	The Msunduzi	The Msunduzi, KwaZulu-Natal	751.991267651700014	district	DC22	KwaZulu-Natal	KZN	B	P O BOX 321	PIETERMARITZBURG	3200	City Hall	Chief Albert Luthuli Street	3201	033 392 3000	033 392 2506	http://www.msunduzi.gov.za	Pietermaritzburg	B1	618536
106	municipality	KZN226	Mkhambathini	Mkhambathini, KwaZulu-Natal	869.48718310905997	district	DC22	KwaZulu-Natal	KZN	B	Private bag X04	Camperdown	3720	Mkhambathini Municipality	18 old main road	3720	031 785 9300	031 785 2121	http://www.mkhambathini.gov.za	Camperdown	B3	63142
174	municipality	KZN227	Richmond	Richmond, KwaZulu-Natal	1232.77837067641008	district	DC22	KwaZulu-Natal	KZN	B	PRIVATE BAG X1028	Richmond	3780	Memorial Hall	57 Shepstone Street	3780	033 212 2155	033 212 4668	http://www.richmond.gov.za	Richmond	B4	65793
107	municipality	KZN232	Emnambithi/Ladysmith	Emnambithi/Ladysmith, KwaZulu-Natal	2964.84000000000015	district	DC23	KwaZulu-Natal	KZN	B	P O BOX 19	LADYSMITH	3370	Lister Clarence Building	Murchison Street	3370	036 637 2231	036 631 0415	http://www.ladysmith.co.za	Ladysmith	B2	237437
108	municipality	KZN233	Indaka	Indaka, KwaZulu-Natal	991.539999999999964	district	DC23	KwaZulu-Natal	KZN	B	P/BAG X 70113	WASBANK	2920	Indaka Local Municipality	2748 "F" Section	Wasbank	2920	034 261 1000	http://034 261 2035	Ekuvukeni T/Ship	B4	103116
109	municipality	KZN234	Umtshezi	Umtshezi, KwaZulu-Natal	1972.45000000000005	district	DC23	KwaZulu-Natal	KZN	B	P O BOX 15	ESTCOURT	3310	Civic Building	Victoria Street	3310	036 342 7800	036 352 5829	http://www.umtshezi.co.za	Estcourt	B3	83153
110	municipality	KZN235	Okhahlamba	Okhahlamba, KwaZulu-Natal	3976.44874065577005	district	DC23	KwaZulu-Natal	KZN	B	P O BOX 71	BERGVILLE	3350	Okhahlamba Municipality	10 Broadway Street	3350	036 448 1076	036 448 1986/2472	http://www.okhahlamba.org.za	Bergville	B4	132068
111	municipality	KZN236	Imbabazane	Imbabazane, KwaZulu-Natal	1426.30999999999995	district	DC23	KwaZulu-Natal	KZN	B	P O BOX 750	ESTCOURT	3310	Ntabamhlophe	1 Sobabili Road	Sobabili Area	036 353 0625	036 353 6661	http://www.imbabazane.org.za	Ntabamhlope	B4	113073
177	municipality	KZN271	Umhlabuyalingana	Umhlabuyalingana, KwaZulu-Natal	4985.44847476213999	district	DC27	KwaZulu-Natal	KZN	B	PRIVATE BAG X901	KWANGWANASE	3973	Umhlabuyalingana Municipal Offices	Manguzi Main Road	3937	035 592 0680	035 592 0672	http://www.umhlabuyalingana.gov.za	Kwangwanase	B4	156736
122	municipality	KZN272	Jozini	Jozini, KwaZulu-Natal	3447.91364374552995	district	DC27	KwaZulu-Natal	KZN	B	PRIVATE BAG X28	JOZINI	3969	Jozini Municipality	Circle Street Bottom Town	3969	035 572 1292	035 572 1266	http://www.jozini.org.za	Jozini	B4	186502
123	municipality	KZN273	The Big 5 False Bay	The Big 5 False Bay, KwaZulu-Natal	2486.53999999999996	district	DC27	KwaZulu-Natal	KZN	B	P.O BOX 89	HLUHLUWE	3960	Library Building	163 Zebra Street	3960	035 562 0040	035 562 0988	http://www.big5falsebay.co.za	Hluhluwe	B3	35258
124	municipality	KZN274	Hlabisa	Hlabisa, KwaZulu-Natal	1555.13000000000011	district	DC27	KwaZulu-Natal	KZN	B	P.O BOX 387	HLABISA	3937	Hlabisa Municipal Offices	Loft 808 Off Masson Street	3937	035 838 8500	035 838 1015	http://www.hlabisa.org.za	Hlabisa	B4	71925
125	municipality	KZN275	Mtubatuba	Mtubatuba, KwaZulu-Natal	1972.72194414183991	district	DC27	KwaZulu-Natal	KZN	B	PO BOX 52	Mtubatuba	3935	Mtubatuba Municipality	Lot 105, iNkosi Mtubatuba Road	3935	035 550 0069	035 550 0060	http://www.mtubatuba.org.za	Mtubatuba	B3	175425
178	municipality	KZN282	uMhlathuze	uMhlathuze, KwaZulu-Natal	1235.07287795054003	district	DC28	KwaZulu-Natal	KZN	B	PRIVATE BAG X 1004	RICHARDS BAY	3900	Civic Centre	5 Mark Strasse CBD	3900	035 907 5000	035 907 5444	http://www.umhlathuze.gov.za	Richards Bay	B1	334459
130	municipality	KZN286	Nkandla	Nkandla, KwaZulu-Natal	1830.12763683791991	district	DC28	KwaZulu-Natal	KZN	B	PRIVATE BAG X161	NKANDLA	3855	Municipal Offices	LOT 293	3855	035 833 2000	035 833 0920	http://www.nkandla.co.za	NKANDLA	B4	114416
126	municipality	KZN281	Mfolozi	Mfolozi, KwaZulu-Natal	1301.64513696596009	district	DC28	KwaZulu-Natal	KZN	B	P O BOX 96	KwaMbonambi	3915	Municipal Bulding	25 Bredelia Street	3915	035 580 1421	035 580 1141	http://www.umfolozi.gov.za	KwaMbonambi	B4	122889
127	municipality	KZN283	Ntambanana	Ntambanana, KwaZulu-Natal	1082.75999999999999	district	DC28	KwaZulu-Natal	KZN	B	PRIVATE BAG X 20066	EMPANGENI	3880	Municipal Offices	Main Bhucanana Road	3880	035 792 7090 / 1 / 2 / 3	035 792 7094	http://www.ntambanana.org.za	Empangeni	B4	74336
128	municipality	KZN284	uMlalazi	uMlalazi, KwaZulu-Natal	2216.92343875016013	district	DC28	KwaZulu-Natal	KZN	B	P O BOX 37	ESHOWE	3815	\N	1 Hutchinson Street	3815	035 473 3337	035 474 2809	http://www.umlalazi.org.za	Eshowe	B4	213601
129	municipality	KZN285	Mthonjaneni	Mthonjaneni, KwaZulu-Natal	1641.01610423493003	district	DC28	KwaZulu-Natal	KZN	B	P O BOX 11	Melmoth	3835	Municipal Buildings	21 Reinhold Street	3835	035 450 2082	035 450 3224	http://www.mthonjaneni.org.za	Melmoth	B3	47818
134	municipality	KZN431	Ingwe	Ingwe, KwaZulu-Natal	1976.20000000000005	district	DC43	KwaZulu-Natal	KZN	B	P O BOX 62	CREIGHTON	3263	Municipal Building	Creighton Main Street	3263	039 833 1038	039 833 1179	http://www.ingwe.gov.za	Creighton	B4	100548
135	municipality	KZN432	Kwa Sani	Kwa Sani, KwaZulu-Natal	1851.90000000000009	district	DC43	KwaZulu-Natal	KZN	B	P O BOX 43	HIMEVILLE	3256	Kwa Sani Municipality	32 Arbuckle Street	3256	033 702 1060	033 702 1148	http://www.kwasani.co.za	Himeville	B3	12898
180	municipality	KZN433	Greater Kokstad	Greater Kokstad, KwaZulu-Natal	2682.58068786117019	district	DC43	KwaZulu-Natal	KZN	B	P O Box 8	Kokstad	4700	\N	75 Hope Street	4700	039 797 6600	039 727 3676	http://www.kokstad.org.za	Kokstad	B2	65981
136	municipality	KZN434	Ubuhlebezwe	Ubuhlebezwe, KwaZulu-Natal	1670.72294333758009	district	DC43	KwaZulu-Natal	KZN	B	PRIVATAE BAG X132	IXOPO	3276	Ubuhlebezwe Municipality	29 Margaret Street	3276	039 834 7700	039 834 1168	http://www.ubuhlebezwe.gov.za	Ixopo	B4	101691
137	municipality	KZN435	Umzimkhulu	Umzimkhulu, KwaZulu-Natal	2438.17302160956979	district	DC43	KwaZulu-Natal	KZN	B	PO BOX 53	Umzimkhulu	3297	Umzimkhulu Municipality	169 Main Street	3297	039 259 5300	039 259 0223	http://www.umzimkhululm.gov.za	Umzimkhulu	B4	180302
175	municipality	KZN241	Endumeni	Endumeni, KwaZulu-Natal	1612.6346641120399	district	DC24	KwaZulu-Natal	KZN	B	PRIVATE BAG X 2024	DUNDEE	3000	Dundee Civic Centre	64 Victoria Street	3000	034 212 2121	034 212 3856	http://www.endumeni.gov.za	Dundee	B3	64862
112	municipality	KZN242	Nqutu	Nqutu, KwaZulu-Natal	1965.13607584420993	district	DC24	KwaZulu-Natal	KZN	B	PRIVATE BAG X 5521	NQUTHU	3135	Nquthu Municipal Offices	Lot 83 Mdlalose Street (Main Office)	3135	034 271 6100	034 271 6111	http://www.nquthu.gov.za	Nquthu	B4	165307
113	municipality	KZN244	Msinga	Msinga, KwaZulu-Natal	2378.49273572085986	district	DC24	KwaZulu-Natal	KZN	B	Private Bag X530	Tugela Ferry	3010	Tugela Ferry	Opposite Home Afffairs	2010	033 493 0762	033 493 0766	http://www.msinga.org.za	Tugela Ferry	B4	177577
114	municipality	KZN245	Umvoti	Umvoti, KwaZulu-Natal	2708.28050786851009	district	DC24	KwaZulu-Natal	KZN	B	P O BOX 71	GREYTOWN	3250	41 Bell Street	Greytown	\N	033 413 9100	033 417 2571	http://www.umvoti.gov.za	3250	B3	103093
115	municipality	KZN252	Newcastle	Newcastle, KwaZulu-Natal	1858.7068862476699	district	DC25	KwaZulu-Natal	KZN	B	PRIVATE BAG X6621	NEWCASTLE	2940	Newcastle Civic Center	37 Murchison Street	2940	034 328 7600	034 312 1570	http://www.newcastle.gov.za	Newcastle	B1	363236
176	municipality	KZN253	Emadlangeni	Emadlangeni, KwaZulu-Natal	3544.97397402542992	district	DC25	KwaZulu-Natal	KZN	B	P O BOX 11	UTRECHT	2980	Emadlangeni Municipality	34 Voor Street	2980	034 331 3041	034 331 4312	http://www.emadlangeni.gov.za	Utrecht	B3	34442
116	municipality	KZN254	Dannhauser	Dannhauser, KwaZulu-Natal	1709.91003536273001	district	DC25	KwaZulu-Natal	KZN	B	PRIVATAE BAG X 1011	DANNHAUSER	3080	Municipal Offices	8 Church Street	3080	034 621 2666	034 621 2342	http://www.dannhauser.gov.za	Dannhauser	B4	102161
119	municipality	KZN263	Abaqulusi	Abaqulusi, KwaZulu-Natal	4320.48063289459969	district	DC26	KwaZulu-Natal	KZN	B	P O BOX 57	Vryheid	3100	Main Building	Corner Mark and High Street	3100	034 982 2133	086 645 2165	http://www.abaqulusi.gov.za	Vryheid	B3	211060
117	municipality	KZN261	eDumbe	eDumbe, KwaZulu-Natal	1945.9236428715501	district	DC26	KwaZulu-Natal	KZN	B	PRIVATE BAG X308	PAULPIETERSBURG	3180	Municipal Offices	10 Hoog Street	3180	034 995 1650	034 995 1192	http://www.edumbe.gov.za	Paulpietersburg	B3	82053
118	municipality	KZN262	uPhongolo	uPhongolo, KwaZulu-Natal	3115.11093803971016	district	DC26	KwaZulu-Natal	KZN	B	P O BOX 191	PONGOLA	3170	Prince Mangosuthu Square	61 Martin Street	3170	034 413 1223	034 413 1706	http://www.uphongolo.org.za	Pongola	B4	127238
120	municipality	KZN265	Nongoma	Nongoma, KwaZulu-Natal	2185.4804352054698	district	DC26	KwaZulu-Natal	KZN	B	P O BOX 84	Nongoma	3950	Nongoma Municipal Offices	103 Main Street	3950	035 831 7500	035 831 3152	http://www.nongoma.org.za	Nongoma	B4	194908
121	municipality	KZN266	Ulundi	Ulundi, KwaZulu-Natal	3255.09687691895988	district	DC26	KwaZulu-Natal	KZN	B	`PRIVATE BAG X17	Ulundi	3838	Civic Centre	Ba81 price mangosuthu Street	3838	035 874 5100	035 870 1164	http://www.ulundi.gov.za	Ulundi	B4	188317
133	municipality	KZN294	Maphumulo	Maphumulo, KwaZulu-Natal	897.080100793339966	district	DC29	KwaZulu-Natal	KZN	B	Private Bag X9405	Maphumulo	4470	Maphumulo Local Municipality	MR LOT 152	4470	032 481 4500	032 480 2053	http://www.maphumuloonline.gov.za	Maphumulo	B4	96724
131	municipality	KZN291	Mandeni	Mandeni, KwaZulu-Natal	546.192418409160041	district	DC29	KwaZulu-Natal	KZN	B	P.O BOX 144	Mandeni	4490	Municipal Offices	2 Kingfisher Road	4490	032 456 8200	032 456 2504	http://www.mandeni.gov.za	Mandeni	B4	138078
179	municipality	KZN292	KwaDukuza	KwaDukuza, KwaZulu-Natal	735.884964763080006	district	DC29	KwaZulu-Natal	KZN	B	P O Box 72	KwaDukuza	4450	Civic Building	14 Chief Albert Luthuli Street	4450	032 437 5000	032 437 5098	http://www.kwadukuza.gov.za	KwaDukuza	B2	231187
132	municipality	KZN293	Ndwedwe	Ndwedwe, KwaZulu-Natal	1094.27009989808994	district	DC29	KwaZulu-Natal	KZN	B	PRIVATE BAG X 503	NDWEDWE	4342	Ndwedwe Court House	P 100 Road	4342	032 532 5000	032 532 5035	http://www.ndwedwe.gov.za	Ndwedwe	B4	140820
172	municipality	ETH	eThekwini	eThekwini, KwaZulu-Natal	2558.88720171044997	province	KZN	KwaZulu-Natal	KZN	A	P.O BOX 1014	DURBAN	4000	City Hall	263 West Street	4001	031 311 1111	031 311 2171	http://www.durban.gov.za	Durban	A	3442361
138	municipality	LIM331	Greater Giyani	Greater Giyani, Limpopo	4181.49567221308007	district	DC33	Limpopo	LIM	B	Private Bag x9559	GIYANI	0826	Greater Giyani Municipality	BA 59 CIVIC CENTRE	0826	015 811 5500	015 812 0268	http://www.greatergiyani.gov.za	GIYANI	B4	244217
139	municipality	LIM332	Greater Letaba	Greater Letaba, Limpopo	1895.33602637197009	district	DC33	Limpopo	LIM	B	P O BOX 36	MODJADJISKLOOF	0835	Civic Centre	169 Botha Street	0835	015 309 9246/7/8	015 309 9419	http://www.greaterletaba.gov.za	Modjadjiskloof	B4	212701
140	municipality	LIM333	Greater Tzaneen	Greater Tzaneen, Limpopo	2903.26222990795986	district	DC33	Limpopo	LIM	B	P O BOX 24	Tzaneen	0850	CIVIC CENTRE	NO.1 AGATHA	0850	015 307 8000	015 307 8049	http://www.tzaneen.gov.za	Tzaneen	B4	390095
181	municipality	LIM334	Ba-Phalaborwa	Ba-Phalaborwa, Limpopo	7506.44414784976016	district	DC33	Limpopo	LIM	B	PRIVATE BAG X1020	PHALABORWA	1390	Ba Phalaborwa Municipality	Cnr. Nelson Mandela & Selati Road	1390	015 780 6300	015 781 0726	http://www.ba-phalaborwa.gov.za	PHALABORWA	B3	150637
141	municipality	LIM335	Maruleng	Maruleng, Limpopo	3570.49457164455998	district	DC33	Limpopo	LIM	B	P O BOX 627	HOEDSPRUIT	1380	Municipal Building	65 Springbok Street	1380	015 793 2409	015 793 2341	http://www.maruleng.gov.za	Hoedspruit	B4	94857
143	municipality	LIM342	Mutale	Mutale, Limpopo	3886.17000000000007	district	DC34	Limpopo	LIM	B	PRIVATE BAG X1254	MUTALE	0956	New Municipal Offices	\N	0956	015 967 9600	015 967 9677	http://www.mutale.gov.za	Mutale	B4	91870
142	municipality	LIM341	Musina	Musina, Limpopo	10372.6540433054397	district	DC34	Limpopo	LIM	B	PRIVATE BAG X611	MUSINA	0900	Musina Civic Centre	21 Irwin Street	0900	015 534 6100	015 534 2513	http://www.musina.gov.za	Musina	B3	68359
145	municipality	LIM344	Makhado	Makhado, Limpopo	7623.58556451041022	district	DC34	Limpopo	LIM	B	Private Bag X2596	Louis Trichardt	0950	Civic Center	Erasmus/Krough Str	0950	015 519 3000	015 516 5084	http://www.makhado.gov.za	Louis Trichardt	B4	516031
146	municipality	LIM351	Blouberg	Blouberg, Limpopo	9563.16561211388034	district	DC35	Limpopo	LIM	B	P.O BOX 1593	senwabarwana	0790	2nd Building	Senwabarwana/Dendron Road	0790	015 505 7100	015 505 0296	http://www.blouberg.gov.za	Senwabarwana	B4	162629
182	municipality	LIM352	Aganang	Aganang, Limpopo	1880.56999999999994	district	DC35	Limpopo	LIM	B	P O BOX 990	JUNO	0748	Ceres	Moletjie	\N	015 295 1400	015 295 1401	http://www.aganang.gov.za	0748	B4	131164
147	municipality	LIM353	Molemole	Molemole, Limpopo	3636.09346629023003	district	DC35	Limpopo	LIM	B	Private Bag X44	MOGWADI	0715	Civic Centre	303 Church Street	0715	015 501 0243	015 501 0419	http://www.molemole.gov.za	MOGWADI	B4	108321
148	municipality	LIM354	Polokwane	Polokwane, Limpopo	5065.25557430778008	district	DC35	Limpopo	LIM	B	P O BOX 111	POLOKWANE	0700	Civic Centre	C/O Bodenstein & Landdros Maree	0699	015 290 2000	015 290 2106	http://www.polokwane.gov.za	Polokwane	B1	628999
149	municipality	LIM355	Lepele-Nkumpi	Lepele-Nkumpi, Limpopo	3491.99829148800018	district	DC35	Limpopo	LIM	B	PRIVATE BAG X07	CHUENESPOORT	0745	170 BA	LEBOWAKGOMO	0737	015 633 4500	015 633 6896	http://www.lepelle-nkumpi.gov.za	POLOKWANE	B4	230350
150	municipality	LIM361	Thabazimbi	Thabazimbi, Limpopo	11214.4060131220904	district	DC36	Limpopo	LIM	B	PO BOX 90	THABAZIMBI	0380	Russels	7th Rietbok	0380	014 777 1525	014 777 1531	http://www.thabazimbi.gov.za	Thabazimbi	B3	85234
151	municipality	LIM362	Lephalale	Lephalale, Limpopo	13826.0510026259999	district	DC36	Limpopo	LIM	B	PRIVATE BAG X136	LEPHALALE	0555	Civic Centre	C/O Joe Slovo & Douwater Ave	0555	014 763 2193	014 763 5662	http://www.lephalale.gov.za	Lephalale	B3	115767
183	municipality	LIM364	Mookgopong	Mookgopong, Limpopo	5688.85000000000036	district	DC36	Limpopo	LIM	B	PRIVATE BAG X340	MOOKGOPONG	0560	Louis Trichart Avenue	Mookgopong	\N	014 743 1111	014 743 2434	\N	0560	B3	35640
152	municipality	LIM365	Modimolle	Modimolle, Limpopo	4677.94999999999982	district	DC36	Limpopo	LIM	B	P O BOX 1008	MODIMOLLE	0510	O R Tambo Square	Harry Gwala	0510	014 718 2000	014 717 1687	http://www.modimolle.gov.za	Modimolle	B3	68513
153	municipality	LIM366	Bela-Bela	Bela-Bela, Limpopo	3413.32677402970012	district	DC36	Limpopo	LIM	B	PRIVATE BAG X 1609	BELA BELA	0480	399 Chris Hani Rd	Chris Hani Drive	0480	014 736 8000	014 736 3288	http://www.belabela.gov.za	Bela Bela	B3	66500
184	municipality	LIM367	Mogalakwena	Mogalakwena, Limpopo	6170.26803213347011	district	DC36	Limpopo	LIM	B	P O BOX 34	MOKOPANE	0600	Mogalakwena Municipality	54 Retief Street	0600	015 491 9600	086 529 8320	http://www.mogalakwena.gov.za	Mokopane	B2	307682
185	municipality	LIM471	Ephraim Mogale	Ephraim Mogale, Limpopo	2015.53500295277991	district	DC47	Limpopo	LIM	B	P O BOX 111	MARBLE HALL	0450	Civic Centre	13 Ficus Street	0450	013 261 8400	013 261 2985	http://www.ephraimmogalelm.gov.za	Marble Hall	B4	123648
186	municipality	LIM472	Elias Motsoaledi	Elias Motsoaledi, Limpopo	3721.01317308462012	district	DC47	Limpopo	LIM	B	P O BOX 48	Groblersdal	0470	Civic Centre	2nd Avenue Grobler Street	0470	013 262 3056	013 262 4530	http://www.eliasmotsoaledi.gov.za	Groblersdal	B4	249363
187	municipality	LIM473	Makhuduthamaga	Makhuduthamaga, Limpopo	2114.15258490435008	district	DC47	Limpopo	LIM	B	PRIVATE BAG X 434	JANE FURSE	1085	Stand No 1	Groblersdal road	1085	013 265 8600	013 265 1975	http://www.makhuduthamaga.gov.za	Jane Furse	B4	274358
188	municipality	LIM474	Fetakgomo	Fetakgomo, Limpopo	1104.52999999999997	district	DC47	Limpopo	LIM	B	P O BOX 818	APEL	0739	Fetakgomo Municipality	Stand No. 1	0740	015 622 8000	015 622 8026	http://www.fetakgomo.gov.za	Mashung	B4	93795
189	municipality	LIM475	Greater Tubatse	Greater Tubatse, Limpopo	4601.96000000000004	district	DC47	Limpopo	LIM	B	P O BOX 206	BURGERSFORT	1150	Greater Tubatse Building	1 Konstia Street	1150	013 231 1000	013 231 7467	http://www.tubatse.gov.za	Burgersfort	B4	335676
190	municipality	MP301	Chief Albert Luthuli	Chief Albert Luthuli, Mpumalanga	5569.92403031920003	district	DC30	Mpumalanga	MP	B	P.O. BOX 24	CAROLINA	1185	Carolina Municipal Offices	28 Church Street	1185	017 843 4000	017 843 4001	http://www.albertluthuli.gov.za	Carolina	B4	186010
191	municipality	MP302	Msukaligwa	Msukaligwa, Mpumalanga	6026.59793895827988	district	DC30	Mpumalanga	MP	B	P.O BOX 48	ERMELO	2350	Civic Centre	C/O Taute & Kerk Street	2350	017 801 3500	017 801 3851	http://www.msukaligwa.gov.za	Ermelo	B2	149377
264	municipality	MP303	Mkhondo	Mkhondo, Mpumalanga	4890.54894699502984	district	DC30	Mpumalanga	MP	B	P O BOX 23	PIET RETIEF	2380	Municipal Building	33 Mark Street	2380	017 826 8100	017 826 8102	http://www.mkhondo.gov.za	Piet Retief	B3	171982
192	municipality	MP304	Dr Pixley Ka Isaka Seme	Dr Pixley Ka Isaka Seme, Mpumalanga	5236.02314812083023	district	DC30	Mpumalanga	MP	B	PRIVATE BAG X 9011	VOLKSRUST	2470	Municipal Buildings	C/O Jourbert & Lainsnekstreets Voortrekk	2470	017 734 6100	017 735 3004	http://pixleykaseme.local.gov.za	Volksrust	B3	83235
193	municipality	MP305	Lekwa	Lekwa, Mpumalanga	4564.86129071654977	district	DC30	Mpumalanga	MP	B	P O BOX 66	STANDERTON	2430	Main Administration Building	Cnr B Naude & M Maiyela Street	2430	017 712 9600	017 712 6808	\N	Standerton	B3	115662
194	municipality	MP306	Dipaleseng	Dipaleseng, Mpumalanga	2649.46291994355988	district	DC30	Mpumalanga	MP	B	P O BOX 10555	BALFOUR	2410	Municipal Building Kruger Square	Cnr Stuart & Joubert Streets	2410	017 773 0055	017 773 0169	http://www.dipaleseng.gov.za	Balfour	B3	42390
195	municipality	MP307	Govan Mbeki	Govan Mbeki, Mpumalanga	2960.05902898790009	district	DC30	Mpumalanga	MP	B	PRIVATE BAG X 1017	SECUNDA	2302	No. 1 Horwood Street	Cba	2302	017 620 6000	017 634 8019	http://www.govanmbeki.gov.za	Secunda	B1	294538
265	municipality	MP311	Victor Khanye	Victor Khanye, Mpumalanga	1570.72122946411992	district	DC31	Mpumalanga	MP	B	P O BOX 6	DELMAS	2210	Municipal Building	C/O Samuel & V/D Walt Streets	2210	013 665 6000	013 665 2913	http://www.delmasmunic.co.za	Delmas	B3	75452
196	municipality	MP312	Emalahleni	Emalahleni, Mpumalanga	2682.69810047495002	district	DC31	Mpumalanga	MP	B	P O BOX 3	EMALAHLENI (MP)	1035	Civic Centre	C/O Arras & Mandela Avenue	1035	013 690 6911	013 690 6207	http://www.emalahleni.gov.za	Emalahleni	B1	395466
197	municipality	MP313	Steve Tshwete	Steve Tshwete, Mpumalanga	3984.14189435103981	district	DC31	Mpumalanga	MP	B	P O BOX 14	MIDDELBURG	1050	Municipal Building	C/O Church & Wanderers Ave	1050	013 249 7000	013 243 2550	http://www.stevetshwetelm.gov.za	Middelburg	B1	229831
198	municipality	MP314	Emakhazeni	Emakhazeni, Mpumalanga	4744.95305624086996	district	DC31	Mpumalanga	MP	B	P O BOX 17	BELFAST	1100	Municipal Building	25 Scheepers Street	1100	013 253 1121	013 253 1889	http://www.emakhazenilm.co.za	Belfast	B2	47216
199	municipality	MP315	Thembisile	Thembisile, Mpumalanga	2389.13487184370979	district	DC31	Mpumalanga	MP	B	PRIVATE BAG X 4041	EMPUMALANGA	0458	Stand No 24	Alongside Moloto Road R573	0458	013 986 9100	013 986 0995	http://www.thembisilehanilm.gov.za	Kwaggafontein	B4	310458
200	municipality	MP316	Dr JS Moroka	Dr JS Moroka, Mpumalanga	1419.39720003744992	district	DC31	Mpumalanga	MP	B	P/BAG X 4012	SIYABUSWA	0472	Municipal Building A 2601/3	Bongimfundo Street	0472	013 973 1101	013 973 0973/4	http://www.drjsmlm.gov.za	Siyabuswa	B4	249705
201	municipality	MP321	Thaba Chweu	Thaba Chweu, Mpumalanga	5730.88437604712999	district	DC32	Mpumalanga	MP	B	P O BOX 61	LYDENBURG	1120	Civic Centre	C/O Central & Viljoen Street	1120	013 235 7300	013 235 1108	http://www.thabachweumun.gov.za	Lydenburg	B3	98387
266	municipality	MP322	Mbombela	Mbombela, Mpumalanga	5394.43000000000029	district	DC32	Mpumalanga	MP	B	P O BOX 45	NELSPRUIT	1200	Civic Centre	1 Nel Street	1200	013 759 9111	013 759 2070	http://www.mbombela.gov.za	Nelspruit	B1	588794
202	municipality	MP323	Umjindi	Umjindi, Mpumalanga	1745.38000000000011	district	DC32	Mpumalanga	MP	B	P O BOX 33	BARBERTON	1300	Municipal Building	Cnr General & De Villiers Street	1300	013 712 8800	013 712 5120	http://www.umjindi.gov.za	Barberton	B3	67156
203	municipality	MP324	Nkomazi	Nkomazi, Mpumalanga	4796.42334768553974	district	DC32	Mpumalanga	MP	B	PRIVATE BAG X101	MALELANE	1320	Civic Centre	9 Park Street	1320	013 790 0245	013 790 0886	http://www.nkomazi.gov.za	Malelane	B4	393030
204	municipality	MP325	Bushbuckridge	Bushbuckridge, Mpumalanga	10270.3722403872707	district	DC32	Mpumalanga	MP	B	PRIVATE BAG X 9308	BUSHBUCKRIDGE	1280	Municipal Complex	R538 Graskop Road	1280	013 799 1842	013 799 1865	http://www.bushbuckridge.gov.za	Bushbuckridge	B4	541248
205	municipality	NW371	Moretele	Moretele, North West	1500.93378930195991	district	DC37	North West	NW	B	PRIVATE BAG X367	MAKAPANSTAD	0404	Municipal Offices	4605 B	0404	012 716 1000	012 716 9999	\N	Mathibestad	B4	186947
206	municipality	NW372	Local Municipality of Madibeng	Local Municipality of Madibeng, North West	3727.54999703476005	district	DC37	North West	NW	B	P O BOX 106	BRITS	0250	Municipal Head Office	53 Van Velden Street	0250	012 318 9100	012 318 9203	http://www.madibeng.gov.za	Brits	B1	477381
267	municipality	NW373	Rustenburg	Rustenburg, North West	3422.84066796128991	district	DC37	North West	NW	B	P O BOX 16	RUSTENBURG	0300	Missionary Mpheni House	C/O Nelson Mandela & Beyers Naude Drive	0300	014 590 3111	014 590 3399	http://www.rustenburg.gov.za	Rustenburg	B1	549575
207	municipality	NW374	Kgetlengrivier	Kgetlengrivier, North West	3980.86112902341983	district	DC37	North West	NW	B	PO BOX 66	KOSTER	0348	Municipal Building	C/O Smuts & De Wit Streets	0348	014 543 2004/5/6	014 543 2004/5/6	http://www.kgetlengrivier.gov.za	Koster	B3	51049
208	municipality	NW375	Moses Kotane	Moses Kotane, North West	5738.03497021242038	district	DC37	North West	NW	B	PRIVATE BAG X1011	MOGWASE	0314	933 Station Road Unit 3	Mogwase Shopping Complex	0314	014 555 1300	014 555 6368	http://www.moseskotane.gov.za	Mogwase	B4	242554
209	municipality	NW381	Ratlou	Ratlou, North West	4893.41623796477961	district	DC38	North West	NW	B	PO BOX 494	STELLA	8650	Ratlou Local Municipality	Delareyville Road	8650	018 330 7000	018 330 7091	\N	Setlagole Village	B4	107339
210	municipality	NW382	Tswaing	Tswaing, North West	5885.46457519637988	district	DC38	North West	NW	B	P O BOX 24	DELAREY VILLE	2770	Tswaing Local Municipality	Cnr De Larey & Government Street	2770	053 948 0900	053 948 1500	http://www.tswaing.gov.za	Delareyville	B3	124218
211	municipality	NW383	Mafikeng	Mafikeng, North West	3652.84091939798009	district	DC38	North West	NW	B	PRIVATE BAG X 63	MMABATHO	2735	Municipal Offices	Cr. Hector Peterson & Unversity Drive	2735	018 389 0111	018 384 4063	http://www.mafikeng.gov.za	Mmabatho	B2	291527
268	municipality	NW384	Ditsobotla	Ditsobotla, North West	6398.66846619393982	district	DC38	North West	NW	B	P O BOX 7	LICHTENBURG	2740	Civic Centre	C/O Nelson Mandela Drive & Transvaal	2740	018 633 3800	018 632 5247	http://www.ditsobotla.co.za	Lichtenburg	B3	168902
212	municipality	NW385	Ramotshere Moiloa	Ramotshere Moiloa, North West	7337.62152768828037	district	DC38	North West	NW	B	P O BOX 92	ZEERUST	2865	Coetzee Street	Cnr Coetzee and President Street	2865	018 642 1081	018 642 1175	http://www.ramotshere.gov.za	ZEERUST	B3	150713
213	municipality	NW392	Naledi	Naledi, North West	7042.04210025085013	district	DC39	North West	NW	B	P O BOX 35	VRYBURG	8600	Civic Centre	Market Street	8601	053 928 2200	053 927 3482 / 6181	http://www.naledilm.co.za	Vryburg	B3	66781
214	municipality	NW393	Mamusa	Mamusa, North West	3620.41174198280987	district	DC39	North West	NW	B	P O BOX 5	SCHWEIZER RENEKE	2780	Municipal Offices	28 Schweizer Street	2780	053 963 1331	053 963 2474	http://www.mamusalm.co.za	Schweizers Reneke	B3	60355
215	municipality	NW394	Greater Taung	Greater Taung, North West	5647.89426816429022	district	DC39	North West	NW	B	P / BAG X 1048	Taung	8580	Greater Taung Admin Building	Station Street	8580	053 994 9400	053 994 3917	http://www.greatertaung.gov.za	Taung	B4	177642
269	municipality	NW396	Lekwa-Teemane	Lekwa-Teemane, North West	3659.45953728110999	district	DC39	North West	NW	B	P O BOX 13	CHRISTIANA	2680	Municipal Building	Cnr Robyn & Dierkie-Uys	2680	053 441 2206	053 441 3735	http://www.lekwateemane.co.za	Christiana	B3	53248
216	municipality	NW397	Kagisano/Molopo	Kagisano/Molopo, North West	23872.8335288572707	district	DC39	North West	NW	B	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	B4	105789
217	municipality	NW401	Ventersdorp	Ventersdorp, North West	3764.05000000000018	district	DC40	North West	NW	B	PRIVATE BAG X 1010	VENTERSDORP	2710	\N	10 Van Tonder Crescent	2710	018 264 2051	018 264 2051	http://www.ventersdorp.co.za	Ventersdorp	B3	56702
218	municipality	NW402	Tlokwe City Council	Tlokwe City Council, North West	2673.67999999999984	district	DC40	North West	NW	B	PRIVATE BAG X1253	POTCHEFSTROOM	2520	Dan Tloome Complex	35 Wolmarans Street	2520	018 299 5151	018 294 8203	http://www.potch.co.za	Potchefstroom	B1	162762
219	municipality	NW403	City of Matlosana	City of Matlosana, North West	3608.58209762903016	district	DC40	North West	NW	B	PO BOX 99	KLERKSDORP	2570	Mayibuye	C/O Braam Fisher & Emily Hobhouse Street	2570	018 406 8507	018 464 2318	http://www.matlosana.org.za	Klerksdorp	B1	398676
220	municipality	NW404	Maquassi Hills	Maquassi Hills, North West	4678.42277015040963	district	DC40	North West	NW	B	P/ BAG X1003	WOLMARANSSTAD	2630	Municipal Offices	Krugerstreet 19	2630	018 596 1051	018 596 1555	\N	Wolmaransstad	B3	77794
221	municipality	NC061	Richtersveld	Richtersveld, Northern Cape	9620.87847071231045	district	DC6	Northern Cape	NC	B	PRIVATE BAG X113	PORT NOLLOTH	8280	Municipal Building	Main Road	8280	027 851 1111	027 851 1101	http://www.richtersveld.gov.za	Port Nolloth	B3	11982
270	municipality	NC062	Nama Khoi	Nama Khoi, Northern Cape	18012.6649568186003	district	DC6	Northern Cape	NC	B	P O BOX 17	SPRINGBOK	8240	Civic Centre	4 Namakwa St	8240	027 718 8100	027 712 1635	http://www.namakhoi.gov.za	Springbok	B3	47041
222	municipality	NC064	Kamiesberg	Kamiesberg, Northern Cape	14223.3516676891395	district	DC6	Northern Cape	NC	B	P O BOX 38	GARIES	8220	\N	22 Hoofstraat	8220	027 652 8000	027 652 8001	http://www.kamiesbergmun.co.za	Garies	B3	10187
223	municipality	NC065	Hantam	Hantam, Northern Cape	39120.1203110446877	district	DC6	Northern Cape	NC	B	PRIVATE BAG X 14	CALVINIA	8190	20 Hoopstraat	Calvinia	\N	027 341 8500	027 341 8501	http://www.hantam.gov.za	8190	B3	21578
224	municipality	NC066	Karoo Hoogland	Karoo Hoogland, Northern Cape	30253.5692941051493	district	DC6	Northern Cape	NC	B	PRIVATE BAG X03	WILLISTON	8920	Karoo Hoogland Municipality	Mulder Street 7	8920	053 391 3003	053 391 3294	http://www.karoohoogland.gov.za	Williston	B3	12588
225	municipality	NC067	Khâi-Ma	Khâi-Ma, Northern Cape	15734.05273672765	district	DC6	Northern Cape	NC	B	P O BOX 108	POFADDER	8890	Municipal Offices	Nuwe Street	8890	054 933 1000	054 933 0252	http://www.khaima.gov.za	Pofadder	B3	12465
271	municipality	NC071	Ubuntu	Ubuntu, Northern Cape	20410.3944097427702	district	DC7	Northern Cape	NC	B	PRIVATE BAG X329	VICTORIA WEST	7070	Municipality Building	78 Church Street	7070	053 621 0026	053 621 0368	http://www.ubuntu.gov.za	Victoria West	B3	18601
226	municipality	NC072	Umsobomvu	Umsobomvu, Northern Cape	6819.93489413719999	district	DC7	Northern Cape	NC	B	PRIVATE BAG X 6	COLESBERG	9795	Civic Centre	21a Church Street	9795	051 753 0777	051 753 0574	http://www.umsobomvumun.co.za	Colesberg	B3	28376
227	municipality	NC073	Emthanjeni	Emthanjeni, Northern Cape	13485.3527114957997	district	DC7	Northern Cape	NC	B	P O BOX 42	DE AAR	7000	\N	45 Voortrekker Street	7000	053 632 9100	053 631 0105	http://www.emthanjeni.co.za	De Aar	B3	42356
228	municipality	NC074	Kareeberg	Kareeberg, Northern Cape	17718.7434117661687	district	DC7	Northern Cape	NC	B	P.O. Box 10	Carnarvon	8925	Kareeberg Municipality	13 Hanau Street	8925	053 382 3012	053 382 3142	http://www.kareeberg.co.za	Carnarvon	B3	11673
229	municipality	NC075	Renosterberg	Renosterberg, Northern Cape	5535.21887887532012	district	DC7	Northern Cape	NC	B	P O BOX 112	PETRUSVILLE	8770	55 School Street	Petrusville	\N	053 663 0041	053 663 0180	\N	8770	B3	10978
230	municipality	NC076	Thembelihle	Thembelihle, Northern Cape	8032.72134839172031	district	DC7	Northern Cape	NC	B	PRIVATE BAG X3	HOPETOWN	8750	\N	Church Street	8750	053 203 0005 / 8 /422	053 203 0490	http://www.thembelihlemunicipality.gov.za	Hopetown	B3	15701
272	municipality	NC077	Siyathemba	Siyathemba, Northern Cape	14744.5327009382599	district	DC7	Northern Cape	NC	B	P.O BOX 16	PRIESKA	8940	Municipal Building - Civic Centre	Victoria Street	8940	053 353 5300	053 353 1386	http://www.siyathemba.gov.za	Prieska	B3	21591
231	municipality	NC078	Siyancuma	Siyancuma, Northern Cape	16775.04420024512	district	DC7	Northern Cape	NC	B	P O BOX 27	DOUGLAS	8730	Civic Centre	Charl Celliers Street	8730	053 298 1810	053 298 2019	http://www.siyancuma.gov.za	Douglas	B3	37076
232	municipality	NC081	Mier	Mier, Northern Cape	22468.4000000000015	district	DC8	Northern Cape	NC	B	P O BOX 178	MIER	8811	Civic Centre	63 Loubos Road	8811	054 531 0019	054 531 0019	\N	Rietfontein	B3	7003
233	municipality	NC082	Kai !Garib	Kai !Garib, Northern Cape	26411.9633900525514	district	DC8	Northern Cape	NC	B	PRIVAATSAK X6	KAKAMAS	8870	Munisipale Kantoor	Elfdelaan 11	8870	054 431 6300	054 431 6301	http://www.kaigarib.gov.za	Kakamas	B3	65869
234	municipality	NC083	//Khara Hais	//Khara Hais, Northern Cape	21779.7999999999993	district	DC8	Northern Cape	NC	B	PRIVATE BAG X 6003	UPINGTON	8800	Civic Centre	2 Market Street	8800	054 338 7000	054 338 7350	http://www.kharahais.gov.za	Upington	B2	93494
235	municipality	NC084	!Kheis	!Kheis, Northern Cape	11121.2962208404006	district	DC8	Northern Cape	NC	B	PRIVATE BAG X 2	GROBLERSHOOP	8850	97 Oranje Street	Groblershoop	\N	054 833 9500	054 833 9509	http://www.kheismun.co.za	8850	B3	16637
273	municipality	NC085	Tsantsabane	Tsantsabane, Northern Cape	18317.6933437650296	district	DC8	Northern Cape	NC	B	P.O BOX 5	POSTMASBURG	8420	Civic Centre	15 Springbok Street	8420	053 313 7300	053 313 1602	http://www.tsantsabane.co.za	Postmasburg	B3	35093
236	municipality	NC086	Kgatelopele	Kgatelopele, Northern Cape	2482.09086140754016	district	DC8	Northern Cape	NC	B	PO BOX 43	DANIELSKUIL	8405	Kgatelopele Municipal Building	222 Barker Street	8405	053 384 8600	053 384 0326	http://www.kgatelopele.gov.za	DANIELSKUIL	B3	18687
237	municipality	NC091	Sol Plaatjie	Sol Plaatjie, Northern Cape	3149.72570372820019	district	DC9	Northern Cape	NC	B	PRIVATE BAG X 5030	KIMBERLEY	8300	Civic Centre	Sol Plaatje Boulevard	8301	053 830 6911	053 833 1005	http://www.solplaatje.org.za	Kimberley	B1	248041
238	municipality	NC092	Dikgatlong	Dikgatlong, Northern Cape	7326.66837195710013	district	DC9	Northern Cape	NC	B	PRIVATE BAG X5	BARKLEY WEST	8375	Civic Centre	Campbell Street	8375	053 531 6500	053 531 0624	\N	Barkly West	B3	46841
239	municipality	NC093	Magareng	Magareng, Northern Cape	1548.68645490276003	district	DC9	Northern Cape	NC	B	P O BOX 10	WARRENTON	8530	Municipal Building	1 Magrieta Prinsloo Street	8530	053 497 3111	053 497 4514	http://www.magareng.gov.za	Warrenton	B3	24204
274	municipality	NC094	Phokwane	Phokwane, Northern Cape	829.406076381879984	district	DC9	Northern Cape	NC	B	PRIVATE BAG X 3	HARTSWATER	8570	Phokwane Municipality	24 Hertzog Street	8570	053 474 9700	053 474 1768	http://www.phokwane.gov.za	Hartswater	B3	63000
240	municipality	NC451	Joe Morolong	Joe Morolong, Northern Cape	20215.0088571077104	district	DC45	Northern Cape	NC	B	P /BAG X117	MOTHIBISTAD	8474	Joe Morolong Municipal Offices	D320 Cardington Road	8474	053 773 9300	053 773 9350	http://www.joemorolong.gov.za	Churchill Village	B4	89530
241	municipality	NC452	Ga-Segonyana	Ga-Segonyana, Northern Cape	4501.97879429955992	district	DC45	Northern Cape	NC	B	PRIVATE BAG X1522	KURUMAN	8460	Municipal Building	Cnr Voortrekker and School Street	8460	053 712 9300	053 712 3581	http://www.ga-segonyana.gov.za	Kuruman	B3	93651
242	municipality	NC453	Gamagara	Gamagara, Northern Cape	2652.12503879845008	district	DC45	Northern Cape	NC	B	P O BOX 1001	KATHU	8446	Gamagara Local Municipality	C/O Hendrik Van Eck & Frikkie Meyer	8446	053 723 6000	053 723 2021	http://www.gamagara.co.za	Kathu	B3	41617
244	municipality	WC011	Matzikama	Matzikama, Western Cape	12992.7106425296606	district	DC1	Western Cape	WC	B	P O BOX 98	VREDENDAL	8160	Municipal Building	37 Church Street	8160	027 201 3300	027 213 3238	http://www.matzikamamun.co.za	VREDENDAL	B3	67147
275	municipality	WC012	Cederberg	Cederberg, Western Cape	8012.76119686042966	district	DC1	Western Cape	WC	B	Private Bag X2	Clanwilliam	8135	Cederberg Municipality	2A Voortrekker Street	8135	027 482 8000	027 482 1933	http://www.cederbergmunicipality.gov.za	Clanwilliam	B3	49768
245	municipality	WC013	Bergrivier	Bergrivier, Western Cape	4409.46093620220017	district	DC1	Western Cape	WC	B	P O BOX 60	PIKETBERG	7320	Municipal Building	13 Church Street	7320	022 913 6000	022 913 1406	http://www.bergmun.org.za	Piketberg	B3	61897
246	municipality	WC014	Saldanha Bay	Saldanha Bay, Western Cape	2016.37551046713997	district	DC1	Western Cape	WC	B	PRIVATE BAG X12	VREDENBURG	7380	Buller Centre	12 Main Road	7380	022 701 7000	022 715 1518	http://www.sbm.gov.za	Vredenburg	B2	99193
247	municipality	WC015	Swartland	Swartland, Western Cape	3708.9536215704502	district	DC1	Western Cape	WC	B	PRIVATE BAG X52	MALMESBURY	7299	\N	Church Street	7299	022 487 9400	022 487 9440	http://www.swartland.org.za	Malmesbury	B3	113762
248	municipality	WC022	Witzenberg	Witzenberg, Western Cape	10758.6638059957604	district	DC2	Western Cape	WC	B	P O BOX 44	CERES	6835	Municipality	50 Voortrekker Street	6835	023 316 1854	023 316 1877	http://www.witzenberg.gov.za	Ceres	B3	115946
249	municipality	WC023	Drakenstein	Drakenstein, Western Cape	1538.26593366046995	district	DC2	Western Cape	WC	B	P O BOX 1	PAARL	7622	Civic Centre	Bergriver Boulevard	7646	021 807 4500	021 807 8054	http://www.drakenstein.gov.za	Paarl	B1	251262
276	municipality	WC024	Stellenbosch	Stellenbosch, Western Cape	831.141338375810051	district	DC2	Western Cape	WC	B	P O BOX 17	STELLENBOSCH	7599	Stellenbosch Town House	Plein Street	7600	021 808 8111	021 808 8200	http://www.stellenbosch.gov.za	Stellenbosch	B1	155733
250	municipality	WC025	Breede Valley	Breede Valley, Western Cape	3835.43801212828021	district	DC2	Western Cape	WC	B	P/BAG X 3046	WORCESTER	6849	Civic Building	C/O Baring & Hoog Street	6850	023 348 2600	023 347 2599	http://www.bvm.gov.za	Worcester	B2	166825
251	municipality	WC026	Langeberg	Langeberg, Western Cape	4519.05863739190045	district	DC2	Western Cape	WC	B	Private Bag X2	Ashton	6715	\N	28 Main Road	6715	023 615 8000	023 615 1563	http://www.langeberg.gov.za	Ashton	B3	97724
254	municipality	WC034	Swellendam	Swellendam, Western Cape	3836.15300610144004	district	DC3	Western Cape	WC	B	P O BOX 20	SWELLENDAM	6740	Swellendam Municipality	49 Voortrek Street	6740	028 514 8500	028 514 2694	http://www.swellenmun.co.za	Swellendam	B3	35916
252	municipality	WC031	Theewaterskloof	Theewaterskloof, Western Cape	3259.95568440404986	district	DC3	Western Cape	WC	B	P O BOX 24	CALEDON	7230	\N	6 Plein Street	7230	028 214 3300	028 214 1289	http://www.twk.org.za	Caledon	B3	108790
253	municipality	WC032	Overstrand	Overstrand, Western Cape	1674.90398565817009	district	DC3	Western Cape	WC	B	P O BOX 20	HERMANUS	7200	Municipal Building	1 Magnolia Street	7200	028 313 8000	028 313 8182	http://www.overstrand.gov.za	Hermanus	B2	80432
277	municipality	WC033	Cape Agulhas	Cape Agulhas, Western Cape	3471.24474217040006	district	DC3	Western Cape	WC	B	P O BOX 51	BREDASDORP	7280	Municipal Offices	1 Dirkie Uys Street	7280	028 425 5500	028 425 1019	http://www.capeagulhas.gov.za	Bredasdorp	B3	33038
255	municipality	WC041	Kannaland	Kannaland, Western Cape	4767.13475968407965	district	DC4	Western Cape	WC	B	P O BOX 32	Ladismith	6655	Kannaland Municipality	30 Church Street	6655	028 551 1023	028 551 1766	http://www.kannaland.gov.za	Ladismith	B3	24767
256	municipality	WC042	Hessequa	Hessequa, Western Cape	5734.10986469168984	district	DC4	Western Cape	WC	B	P O BOX 29	RIVERSDALE	6670	Civic Centre	Van Der Berg Street	6670	028 713 8000	086 401 5202	http://www.hessequa.gov.za	Riversdal	B3	52642
257	municipality	WC043	Mossel Bay	Mossel Bay, Western Cape	2001.58597445686996	district	DC4	Western Cape	WC	B	PRIVATE BAG X 29	MOSSEL BAY	6500	CIVIC BUILDING	101 MARSH STREET	6500	044 606 5000	044 606 5062	http://www.mosselbaymun.co.za	MOSSEL BAY	B2	89430
258	municipality	WC044	George	George, Western Cape	5193.31060056657043	district	DC4	Western Cape	WC	B	P O BOX 19	GEORGE	6530	Civic Centre	71 York Street	6530	044 801 9111	044 801 9175	http://www.george.gov.za	George	B1	193672
278	municipality	WC045	Oudtshoorn	Oudtshoorn, Western Cape	3541.73191050074001	district	DC4	Western Cape	WC	B	P O BOX 255	OUDTSHOORN	6620	CIVIC CENTRE BUILDING	69 Voortrekker Road	6620	044 203 3000	044 203 3104	http://www.oudtmun.gov.za	Oudtshoorn	B2	95933
259	municipality	WC047	Bitou	Bitou, Western Cape	992.151222832750022	district	DC4	Western Cape	WC	B	P O BOX 1002	PLETTENBERG BAY	6600	Municipal Building	1 Sewell Street	6600	044 501 3000	044 533 3485	http://www.plett.gov.za	Plettenberg Bay	B3	49162
260	municipality	WC048	Knysna	Knysna, Western Cape	1109.09750709170999	district	DC4	Western Cape	WC	B	P O BOX 21	KNYSNA	6570	Council Offices	C/O Clyde & Queen Streets	6571	044 302 6300	044 302 6333	http://www.knysna.gov.za	Knysna	B2	68659
261	municipality	WC051	Laingsburg	Laingsburg, Western Cape	8788.70057511492087	district	DC5	Western Cape	WC	B	PRIVATE BAG X 4	LAINGSBURG	6900	\N	2 Van Riebeeck Street	6900	023 551 1019	023 551 1019	http://www.laingsburg.gov.za	Laingsburg	B3	8289
262	municipality	WC052	Prince Albert	Prince Albert, Western Cape	8156.91769690097044	district	DC5	Western Cape	WC	B	PRIVATE BAG X 53	PRINCE ALBERT	6930	23 Church Street	23 Church Street	6930	023 541 1320	023 541 1321	http://www.pamun.gov.za	Prince Albert	B3	13136
263	municipality	WC053	Beaufort West	Beaufort West, Western Cape	21931.0104323708692	district	DC5	Western Cape	WC	B	PRIVATE BAG 582	BEAUFORT WEST	6970	Sanlam Building	112 Donkin Street	6970	023 414 8100	023 414 8105	http://www.beaufortwestmun.co.za	Beaufort West	B3	49586
243	municipality	CPT	City of Cape Town	City of Cape Town, Western Cape	2446.42989002680997	province	WC	Western Cape	WC	A	PRIVATE BAG X9181	CAPE TOWN	8000	Civic Centre	12 Hertzog Boulevard	8001	021 400 1111	\N	http://www.capetown.gov.za	Cape Town	A	3740026
1	district	DC1	West Coast	West Coast, Western Cape	3130.12417700000015	province	WC	Western Cape	WC	C	P O BOX 242	MOORREESBURG	7310	58 Long Street	Moorreesburg	\N	022 433 8400	086 692 6113	http://www.westcoastdm.co.za	7310	C1	391767
2	district	DC10	Cacadu	Cacadu, Eastern Cape	5856.077988	province	EC	Eastern Cape	EC	C	P O BOX 318	PORT ELIZABETH	6000	Standard Bank Building	32 Govan Mbeki Avenue	6000	041 508 7111	041 508 7022	http://www.cacadu.co.za	Port Elizabeth	C1	450584
3	district	DC12	Amathole	Amathole, Eastern Cape	2171.73260900000014	province	EC	Eastern Cape	EC	C	P O BOX 320	EAST LONDON	5200	Amathole District Municipality	40 Cambridge Street	5201	043 701 4000	043 742 0337	http://www.amathole.gov.za	East London	C2	892637
4	district	DC13	Chris Hani	Chris Hani, Eastern Cape	3636.02271599999995	province	EC	Eastern Cape	EC	C	PRIVATE BAG X7121	QUEENSTOWN	5320	15 Bells Road	Queenstown	\N	045 808 4600	045 839 2355	http://www.chrishanidm.gov.za	5320	C2	795462
5	district	DC14	Joe Gqabi	Joe Gqabi, Eastern Cape	2582.56499699999995	province	EC	Eastern Cape	EC	C	P O BOX 102	BARKLY EAST	9786	Joe Gqabi District Municipality	C/ O Graham & Cole Street	9786	045 979 3000	045 979 3028	http://www.jgdm.gov.za	Barkly East	C2	349768
6	district	DC15	O.R.Tambo	O.R.Tambo, Eastern Cape	1216.96672100000001	province	EC	Eastern Cape	EC	C	PRIVAATE BAG X6043	MTHATHA	5099	O R Tambo House	Nelson Mandela Drive	5099	047 501 6400	047 532 4166	http://www.ortambodm.org.za	Mthatha	C2	1364943
7	district	DC16	Xhariep	Xhariep, Free State	3793.00496699999985	province	FS	Free State	FS	C	PRIVATE BAG X136	TROMPSBURG	9913	Xhariep District Municipality	20 Louw Street	9913	051 713 9300	051 713 0461	http://www.xhariep.gov.za	Trompsburg	C1	146259
8	district	DC18	Lejweleputswa	Lejweleputswa, Free State	3216.80298399999992	province	FS	Free State	FS	C	P O BOX 2163	WELKOM	9460	Lejwelputswa District Municipality	Cnr Tempest & Jan Hofmeyer Road	9460	057 353 3094	057 357 4103	http://www.lejwe.co.za	Welkom	C1	627626
9	district	DC19	Thabo Mofutsanyane	Thabo Mofutsanyane, Free State	3351.68450200000007	province	FS	Free State	FS	C	P/BAG X 810	WITSIESHOEK	9870	Old Parliament Building	1 Mampoi Street	9866	058 713 1000	058 713 0940	http://www.thabomofutsanyanadm.co.za	Phuthaditjhaba	C1	736237
10	district	DC2	Cape Winelands	Cape Winelands, Western Cape	2158.7342749999998	province	WC	Western Cape	WC	C	P O BOX 100	STELLENBOSCH	7599	\N	51 Trappe Street	6850	086 265 2630	023 342 8442	http://www.capewinelands.gov.za	Worcester	C1	787490
11	district	DC20	Fezile Dabi	Fezile Dabi, Free State	2082.91201499999988	province	FS	Free State	FS	C	P O BOX 10	SASOLBURG	1947	Fezile Dabi District Municipality	John Voster Road	1947	016 970 8600	016 970 8733	http://www.feziledabi.gov.za	Sasolburg	C1	488036
12	district	DC21	Ugu	Ugu, KwaZulu-Natal	5079.76948100000027	province	KZN	KwaZulu-Natal	KZN	C	P O BOX 33	PORT SHEPSTONE	4240	Ugu District Municipality	28 Connor Street	4240	039 688 5700	039 682 1720	http://www.ugu.org.za	Port Shepstone	C2	722484
13	district	DC22	Umgungundlovu	Umgungundlovu, KwaZulu-Natal	9578.93650499999967	province	KZN	KwaZulu-Natal	KZN	C	P O BOX 3235	PIETERMARITZBURG	3200	Umgungundlovu District	242 Langalibalele Street	3201	033 897 6700	033 342 5502	http://www.umdm.gov.za	Pietermaritzburg	C2	1017763
14	district	DC23	Uthukela	Uthukela, KwaZulu-Natal	1140.83048099999996	province	KZN	KwaZulu-Natal	KZN	C	P. O. Box 116	Ladysmith	3370	uThukela District Municipality	33 Forbes Street	3370	036 638 5100	086 529 8866	http://www.uthukeladm.co.za	Ladysmith	C2	668847
15	district	DC24	Umzinyathi	Umzinyathi, KwaZulu-Natal	8651.94117499999993	province	KZN	KwaZulu-Natal	KZN	C	P O BOX 1965	DUNDEE	3000	39 Victoria Road	Princess Magogo Building	3000	034 218 1945	034 218 1940	http://www.umzinyathi.gov.za	Dundee	C2	510839
16	district	DC25	Amajuba	Amajuba, KwaZulu-Natal	6963.33322099999987	province	KZN	KwaZulu-Natal	KZN	C	Private Bag X6615	Newcastle	2940	B9356 Amajuba Building	Madadeni Township	2940	034 329 7200	034 314 3785	http://www.amajuba.gov.za	Newcastle	C2	499839
17	district	DC26	Zululand	Zululand, KwaZulu-Natal	1491.16610300000002	province	KZN	KwaZulu-Natal	KZN	C	PRIVATE BAG X76	ULUNDI	3838	Princess Silomo Centre	B North 400 Gagane Street	3838	035 874 5500	035 874 5589	http://www.zululand.org.za	Ulundi	C2	803576
18	district	DC27	Umkhanyakude	Umkhanyakude, KwaZulu-Natal	1396.18629099999998	province	KZN	KwaZulu-Natal	KZN	C	P O BOX 449	MKHUZE	3965	Remainder of Harlingen Farm	13433 Kingfisher Road	3965	035 573 8600	035 573 1094	http://www.ukdm.gov.za	Mkhuze	C2	625846
19	district	DC28	Uthungulu	Uthungulu, KwaZulu-Natal	8273.05495800000062	province	KZN	KwaZulu-Natal	KZN	C	PRIVATE BAG X 1025	RICHARDS BAY	3900	King Cetshwayo House	Corner of Krugerrand and Barbados	3900	035 799 2500	035 789 1409	http://www.kingcetshwayo.gov.za	Richards Bay	C2	907519
20	district	DC29	iLembe	iLembe, KwaZulu-Natal	3292.25921299999982	province	KZN	KwaZulu-Natal	KZN	C	P O BOX 1788	KWADUKUZA	4450	Ilembe House	59-61 Mahatma Gandhi Street	4450	032 437 9300	032 437 9584	http://www.ilembe.gov.za	Kwadukuza	C2	606809
21	district	DC3	Overberg	Overberg, Western Cape	1230.11331100000007	province	WC	Western Cape	WC	C	PRIVATE BAG X22	BREDASDORP	7280	Overberg District Municipality	26 Long Street	7280	028 425 1157	028 425 1014	http://www.odm.org.za	Bredasdorp	C1	258176
22	district	DC30	Gert Sibande	Gert Sibande, Mpumalanga	3209.72732200000019	province	MP	Mpumalanga	MP	C	P O BOX 1748	ERMELO	2350	Council Building	Cnr Oosthuise & Joubert	2350	017 801 7000	017 811 1230	http://www.gsibande.gov.za	Ermelo	C1	1043194
23	district	DC31	Nkangala	Nkangala, Mpumalanga	1689.92186500000003	province	MP	Mpumalanga	MP	C	P O BOX 437	MIDDELBURG	1050	Nkangala District Municipality	2a Church Street	1050	013 249 2000	013 249 2114	http://www.nkangaladm.gov.za	Middelburg	C1	1308128
24	district	DC32	Ehlanzeni	Ehlanzeni, Mpumalanga	2813.69942399999991	province	MP	Mpumalanga	MP	C	P O BOX 3333	NELSPRUIT	1200	\N	8 Van Niekerk Street	1200	013 759 8500	013 755 3157	http://www.ehlanzeni.co.za	Nelspruit	C1	1688615
25	district	DC33	Mopani	Mopani, Limpopo	2019.33166699999992	province	LIM	Limpopo	LIM	C	Private Bag X9687	GIYANI	0826	Old parliament Building	Main Road	0826	015 811 6300	015 811 4301	http://www.mopani.gov.za	Giyani	C2	1092507
26	district	DC34	Vhembe	Vhembe, Limpopo	2583.89159299999983	province	LIM	Limpopo	LIM	C	PRIVATE BAG X5006	THOHOYANDOU	0950	Old Parliament Building	Mphephe Street	0950	015 960 2000	015 962 1017	http://www.vhembe.gov.za	Thohoyandou	C2	1294722
27	district	DC35	Capricorn	Capricorn, Limpopo	2190.53465199999982	province	LIM	Limpopo	LIM	C	P O BOX 4100	Polokwane	0700	Capricorn District Municipality	41 Biccard street	0700	015 294 1000	015 295 7288	http://www.cdm.org.za	Polokwane	C2	1261463
28	district	DC36	Waterberg	Waterberg, Limpopo	4531.56430699999964	province	LIM	Limpopo	LIM	C	PRIVATE BAG X1018	MODIMOLLE	0510	Waterberg District Building	Harry Gwala Street	0510	014 718 3300	014 717 3886	http://www.waterberg.gov.za	Modimolle	C1	679336
29	district	DC37	Bojanala	Bojanala, North West	1848.95336300000008	province	NW	North West	NW	C	P.O BOX 1993	RUSTENBURG	0300	Bojanala P D M	Cnr Fatima Bayat & Beyers Naude	0300	014 590 4500	014 597 0306	http://www.bojanala.gov.za	Rustenburg	C1	1507506
30	district	DC38	Ngaka Modiri Molema	Ngaka Modiri Molema, North West	2844.07866800000011	province	NW	North West	NW	C	PRIVATE BAG X2167	MAFIKENG	2745	Ngaka Modiri Molema Dm	Cnr Carrington & 1st Avenue	2735	018 381 9400	018 381 0561	\N	Mafikeng	C2	842699
31	district	DC39	Dr Ruth Segomotsi Mompati	Dr Ruth Segomotsi Mompati, North West	4405.23903799999971	province	NW	North West	NW	C	P O BOX 21	VRYBURG	8600	50 Market Street	Market	8601	053 928 4700	053 927 2401	http://www.rsmompatidm.gov.za	Vryburg	C2	463815
32	district	DC4	Eden	Eden, Western Cape	2345.06392499999993	province	WC	Western Cape	WC	C	P O BOX 12	GEORGE	6530	Eden District Municipality	54 York Street	6530	044 803 1300	044 874 0175	http://www.edendm.co.za	George	C1	574265
33	district	DC40	Dr Kenneth Kaunda	Dr Kenneth Kaunda, North West	1475.93892000000005	province	NW	North West	NW	C	PRIVATE BAG X 5017	KLERKSDORP	2570	Civic Centre	Patmore Road	2620	018 473 8000	018 473 2523	http://www.kaundadistrict.gov.za	Orkney	C1	695934
34	district	DC42	Sedibeng	Sedibeng, Gauteng	4206.52779100000043	province	GT	Gauteng	GT	C	P O BOX 471	VEREENIGING	1930	Council Main Building	C/O Lesley & Beaconsfield Street	1930	016 450 3000	016 455 2573	http://www.sedibeng.gov.za	Vereeniging	C1	916484
35	district	DC43	Harry Gwala	Harry Gwala, KwaZulu-Natal	1061.80334799999991	province	KZN	KwaZulu-Natal	KZN	C	PRIVATE BAG X501	IXOPO	3276	Sisonke District Municipality	40 Main Street	3276	039 834 8700	039 834 1750	http://www.sisonke.gov.za	Ixopo	C2	461420
36	district	DC44	Alfred Nzo	Alfred Nzo, Eastern Cape	1080.05921199999989	province	EC	Eastern Cape	EC	C	PRIVATE BAG X 511	MOUNT AYLIFF	4735	Andm Building	Erf 1400 Ntsizwa Street	4735	039 254 0320	039 254 0343	http://www.andm.gov.za/site/	Mount Ayliff	C2	801344
37	district	DC45	John Taolo Gaetsewe	John Taolo Gaetsewe, Northern Cape	2749.89137100000016	province	NC	Northern Cape	NC	C	P.O BOX 1480	KURUMAN	8460	John Taolo Gaetsewe District	4 Federale Mynbou Str	8460	053 712 8700	053 712 2502	http://www.taologaetsewe.gov.za	Kuruman	C1	224798
38	district	DC47	Sekhukhune	Sekhukhune, Limpopo	1364.58807499999989	province	LIM	Limpopo	LIM	C	PRIVATE BAG X8611	GROBLERSDAL	0470	3 West Street	Groblersdal	\N	013 262 2743	013 262 4303	http://www.sekhukhune.gov.za	0471	C2	1076840
39	district	DC48	West Rand	West Rand, Gauteng	4120.99300399999993	province	GT	Gauteng	GT	C	PRIVATE BAG X033	RANDFONTEIN	1760	Wrdm Building	Cnr 6th & Park Street	1759	011 411 5000	011 411 5071	http://www.wrdm.gov.za	Randfontein	C1	820995
40	district	DC5	Central Karoo	Central Karoo, Western Cape	3907.3087129999999	province	WC	Western Cape	WC	C	PRIVATE BAG X 560	BEAUFORT WEST	6970	Central Karoo Dm	63 Donkin Street	6970	023 449 1000	023 415 1253	http://www.skdm.co.za	Beaufort West	C1	71011
41	district	DC6	Namakwa	Namakwa, Northern Cape	1276.63268599999992	province	NC	Northern Cape	NC	C	PRIVATE BAG X 20	SPRINGBOK	8240	Hendrik Visser Building	Van Riebeeck Street	8240	027 712 8000	027 712 8040	http://www.namakwa-dm.gov.za	Springbok	C1	115841
42	district	DC7	Pixley ka Seme	Pixley ka Seme, Northern Cape	1040.94585400000005	province	NC	Northern Cape	NC	C	PRIVATE BAG X1012	DE AAR	7000	Culvert Road	De Aar	\N	053 631 0891	053 631 2529	http://www.pixley.co.za	7000	C1	186352
43	district	DC8	Z F Mgcawu	Z F Mgcawu, Northern Cape	1032.97298099999989	province	NC	Northern Cape	NC	C	PRIVATE BAG X 6039	UPINGTON	8800	Cnr Hill & Le Roux Street	C/o Upington 26 & Nelson Mandela Drive	8800	054 337 2800	054 337 2888	http://www.zfm-dm.gov.za	UPINGTON	C1	236783
44	district	DC9	Frances Baard	Frances Baard, Northern Cape	1293.09347200000002	province	NC	Northern Cape	NC	C	PRIVATE BAG X6088	KIMBERLEY	8300	51 Drakensberg Ave	Carters Glen	8301	053 838 0911	053 861 1538	http://www.francesbaard.gov.za	Kimberley	C1	382086
\.


--
-- Name: scorecard_geography_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('scorecard_geography_id_seq', 322, true);


--
-- Name: scorecard_geography_geo_level_1b28c178_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY scorecard_geography
    ADD CONSTRAINT scorecard_geography_geo_level_1b28c178_uniq UNIQUE (geo_level, geo_code);


--
-- Name: scorecard_geography_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY scorecard_geography
    ADD CONSTRAINT scorecard_geography_pkey PRIMARY KEY (id);


--
-- Name: scorecard_geography_unique_geo_code; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY scorecard_geography
    ADD CONSTRAINT scorecard_geography_unique_geo_code UNIQUE (geo_code);


--
-- Name: scorecard_geography_2fc6351a; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_2fc6351a ON scorecard_geography USING btree (long_name);


--
-- Name: scorecard_geography_b068931c; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_b068931c ON scorecard_geography USING btree (name);


--
-- Name: scorecard_geography_category_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_category_idx ON scorecard_geography USING btree (category);


--
-- Name: scorecard_geography_dimension_demarcation_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_dimension_demarcation_idx ON scorecard_geography USING btree (geo_code, name);


--
-- Name: scorecard_geography_dimension_municipality_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_dimension_municipality_idx ON scorecard_geography USING btree (category, geo_code, fax_number, long_name, name, parent_code, phone_number, postal_address_1, postal_address_2, postal_address_3, province_code, province_name, street_address_1, street_address_2, street_address_3, street_address_4, url);


--
-- Name: scorecard_geography_fax_number_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_fax_number_idx ON scorecard_geography USING btree (fax_number);


--
-- Name: scorecard_geography_geo_code_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_geo_code_idx ON scorecard_geography USING btree (geo_code);


--
-- Name: scorecard_geography_long_name_d5fe0964_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_long_name_d5fe0964_like ON scorecard_geography USING btree (long_name varchar_pattern_ops);


--
-- Name: scorecard_geography_long_name_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_long_name_idx ON scorecard_geography USING btree (long_name);


--
-- Name: scorecard_geography_name_52e408f6_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_name_52e408f6_like ON scorecard_geography USING btree (name varchar_pattern_ops);


--
-- Name: scorecard_geography_name_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_name_idx ON scorecard_geography USING btree (name);


--
-- Name: scorecard_geography_parent_code_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_parent_code_idx ON scorecard_geography USING btree (parent_code);


--
-- Name: scorecard_geography_phone_number_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_phone_number_idx ON scorecard_geography USING btree (phone_number);


--
-- Name: scorecard_geography_postal_address_1_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_postal_address_1_idx ON scorecard_geography USING btree (postal_address_1);


--
-- Name: scorecard_geography_postal_address_2_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_postal_address_2_idx ON scorecard_geography USING btree (postal_address_2);


--
-- Name: scorecard_geography_postal_address_3_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_postal_address_3_idx ON scorecard_geography USING btree (postal_address_3);


--
-- Name: scorecard_geography_province_code_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_province_code_idx ON scorecard_geography USING btree (province_code);


--
-- Name: scorecard_geography_province_name_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_province_name_idx ON scorecard_geography USING btree (province_name);


--
-- Name: scorecard_geography_street_address_1_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_street_address_1_idx ON scorecard_geography USING btree (street_address_1);


--
-- Name: scorecard_geography_street_address_2_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_street_address_2_idx ON scorecard_geography USING btree (street_address_2);


--
-- Name: scorecard_geography_street_address_3_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_street_address_3_idx ON scorecard_geography USING btree (street_address_3);


--
-- Name: scorecard_geography_street_address_4_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_street_address_4_idx ON scorecard_geography USING btree (street_address_4);


--
-- Name: scorecard_geography_url_idx; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX scorecard_geography_url_idx ON scorecard_geography USING btree (url);


--
-- PostgreSQL database dump complete
--

