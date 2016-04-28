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

DROP INDEX IF EXISTS public.scorecard_geography_name_52e408f6_like;
DROP INDEX IF EXISTS public.scorecard_geography_long_name_d5fe0964_like;
DROP INDEX IF EXISTS public.scorecard_geography_b068931c;
DROP INDEX IF EXISTS public.scorecard_geography_84cdc76c;
DROP INDEX IF EXISTS public.scorecard_geography_2fc6351a;
ALTER TABLE IF EXISTS ONLY public.scorecard_geography DROP CONSTRAINT IF EXISTS scorecard_geography_pkey;
ALTER TABLE IF EXISTS ONLY public.scorecard_geography DROP CONSTRAINT IF EXISTS scorecard_geography_geo_level_1b28c178_uniq;
ALTER TABLE IF EXISTS public.scorecard_geography ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.scorecard_geography_id_seq;
DROP TABLE IF EXISTS public.scorecard_geography;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: scorecard_geography; Type: TABLE; Schema: public; Owner: municipal_finance; Tablespace: 
--

CREATE TABLE scorecard_geography (
    id integer NOT NULL,
    geo_level character varying(15) NOT NULL,
    geo_code character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    long_name character varying(100),
    year integer,
    square_kms double precision,
    parent_level character varying(15),
    parent_code character varying(10),
    province_name character varying(100) NOT NULL,
    province_code character varying(5) NOT NULL,
    category character varying(2) NOT NULL
);


ALTER TABLE scorecard_geography OWNER TO municipal_finance;

--
-- Name: scorecard_geography_id_seq; Type: SEQUENCE; Schema: public; Owner: municipal_finance
--

CREATE SEQUENCE scorecard_geography_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE scorecard_geography_id_seq OWNER TO municipal_finance;

--
-- Name: scorecard_geography_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: municipal_finance
--

ALTER SEQUENCE scorecard_geography_id_seq OWNED BY scorecard_geography.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: municipal_finance
--

ALTER TABLE ONLY scorecard_geography ALTER COLUMN id SET DEFAULT nextval('scorecard_geography_id_seq'::regclass);


--
-- Data for Name: scorecard_geography; Type: TABLE DATA; Schema: public; Owner: municipal_finance
--

COPY scorecard_geography (id, geo_level, geo_code, name, long_name, year, square_kms, parent_level, parent_code, province_name, province_code, category) FROM stdin;
155	municipality	EC101	Camdeboo	Camdeboo, Eastern Cape	2011	12422.1000000000004	district	DC10	Eastern Cape	EC	B
56	municipality	EC102	Blue Crane Route	Blue Crane Route, Eastern Cape	2011	11068.6000000000004	district	DC10	Eastern Cape	EC	B
59	municipality	EC106	Sundays River Valley	Sundays River Valley, Eastern Cape	2011	5993.52000000000044	district	DC10	Eastern Cape	EC	B
161	municipality	EC157	King Sabata Dalindyebo	King Sabata Dalindyebo, Eastern Cape	2011	3027.36999999999989	district	DC15	Eastern Cape	EC	B
165	municipality	FS196	Mantsopa	Mantsopa, Free State	2011	4290.59000000000015	district	DC19	Free State	FS	B
92	municipality	GT423	Lesedi	Lesedi, Gauteng	2011	1484.3900000000001	district	DC42	Gauteng	GT	B
169	municipality	GT484	Merafong City	Merafong City, Gauteng	2011	1630.53999999999996	district	DC48	Gauteng	GT	B
144	municipality	LIM343	Thulamela	Thulamela, Limpopo	2011	5834.25	district	DC34	Limpopo	LIM	B
204	municipality	MP325	Bushbuckridge	Bushbuckridge, Mpumalanga	2011	10249.7000000000007	district	DC32	Mpumalanga	MP	B
162	municipality	NMA	Nelson Mandela Bay	Nelson Mandela Bay, Eastern Cape	2011	1958.91000000000008	province	EC	Eastern Cape	EC	A
167	municipality	EKU	Ekurhuleni	Ekurhuleni, Gauteng	2011	1975.25999999999999	province	GT	Gauteng	GT	A
170	municipality	JHB	City of Johannesburg	City of Johannesburg, Gauteng	2011	1644.98000000000002	province	GT	Gauteng	GT	A
171	municipality	TSH	City of Tshwane	City of Tshwane, Gauteng	2011	6297.88000000000011	province	GT	Gauteng	GT	A
172	municipality	ETH	eThekwini	eThekwini, KwaZulu-Natal	2011	2291.30999999999995	province	KZN	KwaZulu-Natal	KZN	A
19	district	DC28	Uthungulu	Uthungulu, KwaZulu-Natal	2011	8273.05495800000062	province	KZN	KwaZulu-Natal	KZN	C
20	district	DC29	iLembe	iLembe, KwaZulu-Natal	2011	3292.25921299999982	province	KZN	KwaZulu-Natal	KZN	C
21	district	DC3	Overberg	Overberg, Western Cape	2011	1230.11331100000007	province	WC	Western Cape	WC	C
22	district	DC30	Gert Sibande	Gert Sibande, Mpumalanga	2011	3209.72732200000019	province	MP	Mpumalanga	MP	C
23	district	DC31	Nkangala	Nkangala, Mpumalanga	2011	1689.92186500000003	province	MP	Mpumalanga	MP	C
24	district	DC32	Ehlanzeni	Ehlanzeni, Mpumalanga	2011	2813.69942399999991	province	MP	Mpumalanga	MP	C
25	district	DC33	Mopani	Mopani, Limpopo	2011	2019.33166699999992	province	LIM	Limpopo	LIM	C
26	district	DC34	Vhembe	Vhembe, Limpopo	2011	2583.89159299999983	province	LIM	Limpopo	LIM	C
27	district	DC35	Capricorn	Capricorn, Limpopo	2011	2190.53465199999982	province	LIM	Limpopo	LIM	C
28	district	DC36	Waterberg	Waterberg, Limpopo	2011	4531.56430699999964	province	LIM	Limpopo	LIM	C
29	district	DC37	Bojanala	Bojanala, North West	2011	1848.95336300000008	province	NW	North West	NW	C
30	district	DC38	Ngaka Modiri Molema	Ngaka Modiri Molema, North West	2011	2844.07866800000011	province	NW	North West	NW	C
31	district	DC39	Dr Ruth Segomotsi Mompati	Dr Ruth Segomotsi Mompati, North West	2011	4405.23903799999971	province	NW	North West	NW	C
32	district	DC4	Eden	Eden, Western Cape	2011	2345.06392499999993	province	WC	Western Cape	WC	C
33	district	DC40	Dr Kenneth Kaunda	Dr Kenneth Kaunda, North West	2011	1475.93892000000005	province	NW	North West	NW	C
34	district	DC42	Sedibeng	Sedibeng, Gauteng	2011	4206.52779100000043	province	GT	Gauteng	GT	C
35	district	DC43	Sisonke	Sisonke, KwaZulu-Natal	2011	1061.80334799999991	province	KZN	KwaZulu-Natal	KZN	C
36	district	DC44	Alfred Nzo	Alfred Nzo, Eastern Cape	2011	1080.05921199999989	province	EC	Eastern Cape	EC	C
37	district	DC45	John Taolo Gaetsewe	John Taolo Gaetsewe, Northern Cape	2011	2749.89137100000016	province	NC	Northern Cape	NC	C
38	district	DC47	Sekhukhune	Sekhukhune, Limpopo	2011	1364.58807499999989	province	LIM	Limpopo	LIM	C
39	district	DC48	West Rand	West Rand, Gauteng	2011	4120.99300399999993	province	GT	Gauteng	GT	C
40	district	DC5	Central Karoo	Central Karoo, Western Cape	2011	3907.3087129999999	province	WC	Western Cape	WC	C
41	district	DC6	Namakwa	Namakwa, Northern Cape	2011	1276.63268599999992	province	NC	Northern Cape	NC	C
42	district	DC7	Pixley ka Seme	Pixley ka Seme, Northern Cape	2011	1040.94585400000005	province	NC	Northern Cape	NC	C
43	district	DC8	Siyanda	Siyanda, Northern Cape	2011	1032.97298099999989	province	NC	Northern Cape	NC	C
44	district	DC9	Frances Baard	Frances Baard, Northern Cape	2011	1293.09347200000002	province	NC	Northern Cape	NC	C
1	district	DC1	West Coast	West Coast, Western Cape	2011	3130.12417700000015	province	WC	Western Cape	WC	C
2	district	DC10	Cacadu	Cacadu, Eastern Cape	2011	5856.077988	province	EC	Eastern Cape	EC	C
3	district	DC12	Amathole	Amathole, Eastern Cape	2011	2171.73260900000014	province	EC	Eastern Cape	EC	C
4	district	DC13	Chris Hani	Chris Hani, Eastern Cape	2011	3636.02271599999995	province	EC	Eastern Cape	EC	C
5	district	DC14	Joe Gqabi	Joe Gqabi, Eastern Cape	2011	2582.56499699999995	province	EC	Eastern Cape	EC	C
6	district	DC15	O.R.Tambo	O.R.Tambo, Eastern Cape	2011	1216.96672100000001	province	EC	Eastern Cape	EC	C
7	district	DC16	Xhariep	Xhariep, Free State	2011	3793.00496699999985	province	FS	Free State	FS	C
8	district	DC18	Lejweleputswa	Lejweleputswa, Free State	2011	3216.80298399999992	province	FS	Free State	FS	C
9	district	DC19	Thabo Mofutsanyane	Thabo Mofutsanyane, Free State	2011	3351.68450200000007	province	FS	Free State	FS	C
10	district	DC2	Cape Winelands	Cape Winelands, Western Cape	2011	2158.7342749999998	province	WC	Western Cape	WC	C
11	district	DC20	Fezile Dabi	Fezile Dabi, Free State	2011	2082.91201499999988	province	FS	Free State	FS	C
12	district	DC21	Ugu	Ugu, KwaZulu-Natal	2011	5079.76948100000027	province	KZN	KwaZulu-Natal	KZN	C
13	district	DC22	Umgungundlovu	Umgungundlovu, KwaZulu-Natal	2011	9578.93650499999967	province	KZN	KwaZulu-Natal	KZN	C
14	district	DC23	Uthukela	Uthukela, KwaZulu-Natal	2011	1140.83048099999996	province	KZN	KwaZulu-Natal	KZN	C
15	district	DC24	Umzinyathi	Umzinyathi, KwaZulu-Natal	2011	8651.94117499999993	province	KZN	KwaZulu-Natal	KZN	C
16	district	DC25	Amajuba	Amajuba, KwaZulu-Natal	2011	6963.33322099999987	province	KZN	KwaZulu-Natal	KZN	C
17	district	DC26	Zululand	Zululand, KwaZulu-Natal	2011	1491.16610300000002	province	KZN	KwaZulu-Natal	KZN	C
18	district	DC27	Umkhanyakude	Umkhanyakude, KwaZulu-Natal	2011	1396.18629099999998	province	KZN	KwaZulu-Natal	KZN	C
57	municipality	EC103	Ikwezi	Ikwezi, Eastern Cape	2011	4562.72999999999956	district	DC10	Eastern Cape	EC	B
58	municipality	EC104	Makana	Makana, Eastern Cape	2011	4375.63000000000011	district	DC10	Eastern Cape	EC	B
60	municipality	EC107	Baviaans	Baviaans, Eastern Cape	2011	11668.2999999999993	district	DC10	Eastern Cape	EC	B
61	municipality	EC108	Kouga	Kouga, Eastern Cape	2011	2669.82000000000016	district	DC10	Eastern Cape	EC	B
62	municipality	EC109	Kou-Kamma	Kou-Kamma, Eastern Cape	2011	3642.01999999999998	district	DC10	Eastern Cape	EC	B
63	municipality	EC121	Mbhashe	Mbhashe, Eastern Cape	2011	3169.44999999999982	district	DC12	Eastern Cape	EC	B
64	municipality	EC123	Great Kei	Great Kei, Eastern Cape	2011	1735.99000000000001	district	DC12	Eastern Cape	EC	B
65	municipality	EC124	Amahlathi	Amahlathi, Eastern Cape	2011	4820.22000000000025	district	DC12	Eastern Cape	EC	B
66	municipality	EC126	Ngqushwa	Ngqushwa, Eastern Cape	2011	2240.90999999999985	district	DC12	Eastern Cape	EC	B
67	municipality	EC127	Nkonkobe	Nkonkobe, Eastern Cape	2011	3626.17999999999984	district	DC12	Eastern Cape	EC	B
68	municipality	EC131	Inxuba Yethemba	Inxuba Yethemba, Eastern Cape	2011	11662.7000000000007	district	DC13	Eastern Cape	EC	B
69	municipality	EC132	Tsolwana	Tsolwana, Eastern Cape	2011	6086.81999999999971	district	DC13	Eastern Cape	EC	B
70	municipality	EC133	Inkwanca	Inkwanca, Eastern Cape	2011	3584.23999999999978	district	DC13	Eastern Cape	EC	B
71	municipality	EC134	Lukanji	Lukanji, Eastern Cape	2011	3812.86000000000013	district	DC13	Eastern Cape	EC	B
72	municipality	EC136	Emalahleni	Emalahleni, Eastern Cape	2011	3447.19999999999982	district	DC13	Eastern Cape	EC	B
73	municipality	EC137	Engcobo	Engcobo, Eastern Cape	2011	2483.86999999999989	district	DC13	Eastern Cape	EC	B
74	municipality	EC138	Sakhisizwe	Sakhisizwe, Eastern Cape	2011	2354.7199999999998	district	DC13	Eastern Cape	EC	B
75	municipality	EC141	Elundini	Elundini, Eastern Cape	2011	5064.53999999999996	district	DC14	Eastern Cape	EC	B
76	municipality	EC142	Senqu	Senqu, Eastern Cape	2011	7329.42000000000007	district	DC14	Eastern Cape	EC	B
77	municipality	EC143	Maletswai	Maletswai, Eastern Cape	2011	4357.64999999999964	district	DC14	Eastern Cape	EC	B
78	municipality	EC153	Ngquza Hill	Ngquza Hill, Eastern Cape	2011	2476.82999999999993	district	DC15	Eastern Cape	EC	B
51	municipality	EC154	Port St Johns	Port St Johns, Eastern Cape	2011	1291.20000000000005	district	DC15	Eastern Cape	EC	B
52	municipality	EC155	Nyandeni	Nyandeni, Eastern Cape	2011	2474.01000000000022	district	DC15	Eastern Cape	EC	B
79	municipality	EC156	Mhlontlo	Mhlontlo, Eastern Cape	2011	2826.09000000000015	district	DC15	Eastern Cape	EC	B
80	municipality	EC441	Matatiele	Matatiele, Eastern Cape	2011	4352.3100000000004	district	DC44	Eastern Cape	EC	B
45	municipality	EC442	Umzimvubu	Umzimvubu, Eastern Cape	2011	2577.23000000000002	district	DC44	Eastern Cape	EC	B
46	municipality	EC443	Mbizana	Mbizana, Eastern Cape	2011	2416.7199999999998	district	DC44	Eastern Cape	EC	B
47	municipality	EC444	Ntabankulu	Ntabankulu, Eastern Cape	2011	1384.96000000000004	district	DC44	Eastern Cape	EC	B
48	municipality	FS161	Letsemeng	Letsemeng, Free State	2011	9828.57999999999993	district	DC16	Free State	FS	B
49	municipality	FS162	Kopanong	Kopanong, Free State	2011	15645.1000000000004	district	DC16	Free State	FS	B
50	municipality	FS163	Mohokare	Mohokare, Free State	2011	8775.97999999999956	district	DC16	Free State	FS	B
53	municipality	FS181	Masilonyana	Masilonyana, Free State	2011	6796.09000000000015	district	DC18	Free State	FS	B
54	municipality	FS182	Tokologo	Tokologo, Free State	2011	9325.86000000000058	district	DC18	Free State	FS	B
55	municipality	FS183	Tswelopele	Tswelopele, Free State	2011	6524.06999999999971	district	DC18	Free State	FS	B
81	municipality	FS184	Matjhabeng	Matjhabeng, Free State	2011	5155.46000000000004	district	DC18	Free State	FS	B
82	municipality	FS185	Nala	Nala, Free State	2011	4128.80000000000018	district	DC18	Free State	FS	B
83	municipality	FS192	Dihlabeng	Dihlabeng, Free State	2011	4879.96000000000004	district	DC19	Free State	FS	B
84	municipality	FS193	Nketoana	Nketoana, Free State	2011	5611.11999999999989	district	DC19	Free State	FS	B
85	municipality	FS194	Maluti a Phofung	Maluti a Phofung, Free State	2011	4337.67000000000007	district	DC19	Free State	FS	B
86	municipality	FS195	Phumelela	Phumelela, Free State	2011	8183.43000000000029	district	DC19	Free State	FS	B
87	municipality	FS201	Moqhaka	Moqhaka, Free State	2011	7924.5600000000004	district	DC20	Free State	FS	B
88	municipality	FS203	Ngwathe	Ngwathe, Free State	2011	7055.01000000000022	district	DC20	Free State	FS	B
89	municipality	FS204	Metsimaholo	Metsimaholo, Free State	2011	1717.09999999999991	district	DC20	Free State	FS	B
90	municipality	FS205	Mafube	Mafube, Free State	2011	3971.36000000000013	district	DC20	Free State	FS	B
91	municipality	GT421	Emfuleni	Emfuleni, Gauteng	2011	965.894000000000005	district	DC42	Gauteng	GT	B
93	municipality	GT481	Mogale City	Mogale City, Gauteng	2011	1342.16000000000008	district	DC48	Gauteng	GT	B
94	municipality	GT482	Randfontein	Randfontein, Gauteng	2011	474.894000000000005	district	DC48	Gauteng	GT	B
95	municipality	GT483	Westonaria	Westonaria, Gauteng	2011	639.823999999999955	district	DC48	Gauteng	GT	B
96	municipality	KZN211	Vulamehlo	Vulamehlo, KwaZulu-Natal	2011	959.923999999999978	district	DC21	KwaZulu-Natal	KZN	B
97	municipality	KZN212	Umdoni	Umdoni, KwaZulu-Natal	2011	251.52600000000001	district	DC21	KwaZulu-Natal	KZN	B
98	municipality	KZN213	Umzumbe	Umzumbe, KwaZulu-Natal	2011	1258.88000000000011	district	DC21	KwaZulu-Natal	KZN	B
99	municipality	KZN214	UMuziwabantu	UMuziwabantu, KwaZulu-Natal	2011	1089.47000000000003	district	DC21	KwaZulu-Natal	KZN	B
100	municipality	KZN215	Ezingoleni	Ezingoleni, KwaZulu-Natal	2011	648.07000000000005	district	DC21	KwaZulu-Natal	KZN	B
101	municipality	KZN221	uMshwathi	uMshwathi, KwaZulu-Natal	2011	1817.94000000000005	district	DC22	KwaZulu-Natal	KZN	B
102	municipality	KZN222	uMngeni	uMngeni, KwaZulu-Natal	2011	1566.51999999999998	district	DC22	KwaZulu-Natal	KZN	B
103	municipality	KZN223	Mpofana	Mpofana, KwaZulu-Natal	2011	1819.78999999999996	district	DC22	KwaZulu-Natal	KZN	B
104	municipality	KZN224	Impendle	Impendle, KwaZulu-Natal	2011	1528.19000000000005	district	DC22	KwaZulu-Natal	KZN	B
105	municipality	KZN225	The Msunduzi	The Msunduzi, KwaZulu-Natal	2011	634.010999999999967	district	DC22	KwaZulu-Natal	KZN	B
156	municipality	EC105	Ndlambe	Ndlambe, Eastern Cape	2011	1840.63000000000011	district	DC10	Eastern Cape	EC	B
157	municipality	EC122	Mnquma	Mnquma, Eastern Cape	2011	3270.23999999999978	district	DC12	Eastern Cape	EC	B
158	municipality	EC128	Nxuba	Nxuba, Eastern Cape	2011	2731.92000000000007	district	DC12	Eastern Cape	EC	B
159	municipality	EC135	Intsika Yethu	Intsika Yethu, Eastern Cape	2011	2711.13999999999987	district	DC13	Eastern Cape	EC	B
160	municipality	EC144	Gariep	Gariep, Eastern Cape	2011	8911.05999999999949	district	DC14	Eastern Cape	EC	B
163	municipality	FS164	Naledi	Naledi, Free State	2011	3424.05999999999995	district	DC16	Free State	FS	B
164	municipality	FS191	Setsoto	Setsoto, Free State	2011	5966.35999999999967	district	DC19	Free State	FS	B
106	municipality	KZN226	Mkhambathini	Mkhambathini, KwaZulu-Natal	2011	890.875999999999976	district	DC22	KwaZulu-Natal	KZN	B
107	municipality	KZN232	Emnambithi/Ladysmith	Emnambithi/Ladysmith, KwaZulu-Natal	2011	2964.84000000000015	district	DC23	KwaZulu-Natal	KZN	B
108	municipality	KZN233	Indaka	Indaka, KwaZulu-Natal	2011	991.539999999999964	district	DC23	KwaZulu-Natal	KZN	B
109	municipality	KZN234	Umtshezi	Umtshezi, KwaZulu-Natal	2011	1972.45000000000005	district	DC23	KwaZulu-Natal	KZN	B
110	municipality	KZN235	Okhahlamba	Okhahlamba, KwaZulu-Natal	2011	3970.98000000000002	district	DC23	KwaZulu-Natal	KZN	B
111	municipality	KZN236	Imbabazane	Imbabazane, KwaZulu-Natal	2011	1426.30999999999995	district	DC23	KwaZulu-Natal	KZN	B
112	municipality	KZN242	Nqutu	Nqutu, KwaZulu-Natal	2011	1962.25999999999999	district	DC24	KwaZulu-Natal	KZN	B
113	municipality	KZN244	Msinga	Msinga, KwaZulu-Natal	2011	2501.13999999999987	district	DC24	KwaZulu-Natal	KZN	B
114	municipality	KZN245	Umvoti	Umvoti, KwaZulu-Natal	2011	2515.5300000000002	district	DC24	KwaZulu-Natal	KZN	B
115	municipality	KZN252	Newcastle	Newcastle, KwaZulu-Natal	2011	1855.28999999999996	district	DC25	KwaZulu-Natal	KZN	B
116	municipality	KZN254	Dannhauser	Dannhauser, KwaZulu-Natal	2011	1515.91000000000008	district	DC25	KwaZulu-Natal	KZN	B
117	municipality	KZN261	eDumbe	eDumbe, KwaZulu-Natal	2011	1942.75999999999999	district	DC26	KwaZulu-Natal	KZN	B
118	municipality	KZN262	UPhongolo	UPhongolo, KwaZulu-Natal	2011	3239.19000000000005	district	DC26	KwaZulu-Natal	KZN	B
119	municipality	KZN263	Abaqulusi	Abaqulusi, KwaZulu-Natal	2011	4184.63000000000011	district	DC26	KwaZulu-Natal	KZN	B
120	municipality	KZN265	Nongoma	Nongoma, KwaZulu-Natal	2011	2182.11000000000013	district	DC26	KwaZulu-Natal	KZN	B
121	municipality	KZN266	Ulundi	Ulundi, KwaZulu-Natal	2011	3250.28999999999996	district	DC26	KwaZulu-Natal	KZN	B
122	municipality	KZN272	Jozini	Jozini, KwaZulu-Natal	2011	3442.25	district	DC27	KwaZulu-Natal	KZN	B
123	municipality	KZN273	The Big 5 False Bay	The Big 5 False Bay, KwaZulu-Natal	2011	2486.53999999999996	district	DC27	KwaZulu-Natal	KZN	B
124	municipality	KZN274	Hlabisa	Hlabisa, KwaZulu-Natal	2011	1555.13000000000011	district	DC27	KwaZulu-Natal	KZN	B
125	municipality	KZN275	Mtubatuba	Mtubatuba, KwaZulu-Natal	2011	1969.83999999999992	district	DC27	KwaZulu-Natal	KZN	B
126	municipality	KZN281	Mfolozi	Mfolozi, KwaZulu-Natal	2011	1209.98000000000002	district	DC28	KwaZulu-Natal	KZN	B
127	municipality	KZN283	Ntambanana	Ntambanana, KwaZulu-Natal	2011	1082.75999999999999	district	DC28	KwaZulu-Natal	KZN	B
128	municipality	KZN284	uMlalazi	uMlalazi, KwaZulu-Natal	2011	2213.94000000000005	district	DC28	KwaZulu-Natal	KZN	B
129	municipality	KZN285	Mthonjaneni	Mthonjaneni, KwaZulu-Natal	2011	1085.97000000000003	district	DC28	KwaZulu-Natal	KZN	B
130	municipality	KZN286	Nkandla	Nkandla, KwaZulu-Natal	2011	1827.57999999999993	district	DC28	KwaZulu-Natal	KZN	B
131	municipality	KZN291	Mandeni	Mandeni, KwaZulu-Natal	2011	545.480999999999995	district	DC29	KwaZulu-Natal	KZN	B
132	municipality	KZN293	Ndwedwe	Ndwedwe, KwaZulu-Natal	2011	1092.8900000000001	district	DC29	KwaZulu-Natal	KZN	B
133	municipality	KZN294	Maphumulo	Maphumulo, KwaZulu-Natal	2011	895.908999999999992	district	DC29	KwaZulu-Natal	KZN	B
134	municipality	KZN431	Ingwe	Ingwe, KwaZulu-Natal	2011	1976.20000000000005	district	DC43	KwaZulu-Natal	KZN	B
135	municipality	KZN432	Kwa Sani	Kwa Sani, KwaZulu-Natal	2011	1851.90000000000009	district	DC43	KwaZulu-Natal	KZN	B
136	municipality	KZN434	Ubuhlebezwe	Ubuhlebezwe, KwaZulu-Natal	2011	1604.02999999999997	district	DC43	KwaZulu-Natal	KZN	B
137	municipality	KZN435	Umzimkhulu	Umzimkhulu, KwaZulu-Natal	2011	2435.4699999999998	district	DC43	KwaZulu-Natal	KZN	B
138	municipality	LIM331	Greater Giyani	Greater Giyani, Limpopo	2011	4171.60999999999967	district	DC33	Limpopo	LIM	B
139	municipality	LIM332	Greater Letaba	Greater Letaba, Limpopo	2011	1890.8900000000001	district	DC33	Limpopo	LIM	B
140	municipality	LIM333	Greater Tzaneen	Greater Tzaneen, Limpopo	2011	3242.57999999999993	district	DC33	Limpopo	LIM	B
141	municipality	LIM335	Maruleng	Maruleng, Limpopo	2011	3244.30000000000018	district	DC33	Limpopo	LIM	B
142	municipality	LIM341	Musina	Musina, Limpopo	2011	7576.82999999999993	district	DC34	Limpopo	LIM	B
143	municipality	LIM342	Mutale	Mutale, Limpopo	2011	3886.17000000000007	district	DC34	Limpopo	LIM	B
145	municipality	LIM344	Makhado	Makhado, Limpopo	2011	8299.70000000000073	district	DC34	Limpopo	LIM	B
146	municipality	LIM351	Blouberg	Blouberg, Limpopo	2011	9248.1200000000008	district	DC35	Limpopo	LIM	B
147	municipality	LIM353	Molemole	Molemole, Limpopo	2011	3347.32999999999993	district	DC35	Limpopo	LIM	B
148	municipality	LIM354	Polokwane	Polokwane, Limpopo	2011	3765.98000000000002	district	DC35	Limpopo	LIM	B
149	municipality	LIM355	Lepele-Nkumpi	Lepele-Nkumpi, Limpopo	2011	3463.44999999999982	district	DC35	Limpopo	LIM	B
150	municipality	LIM361	Thabazimbi	Thabazimbi, Limpopo	2011	11190.1000000000004	district	DC36	Limpopo	LIM	B
151	municipality	LIM362	Lephalale	Lephalale, Limpopo	2011	13784.2000000000007	district	DC36	Limpopo	LIM	B
152	municipality	LIM365	Modimolle	Modimolle, Limpopo	2011	4677.94999999999982	district	DC36	Limpopo	LIM	B
153	municipality	LIM366	Bela-Bela	Bela-Bela, Limpopo	2011	3406.19999999999982	district	DC36	Limpopo	LIM	B
154	municipality	BUF	Buffalo City	Buffalo City, Eastern Cape	2011	2535.92999999999984	province	EC	Eastern Cape	EC	A
168	municipality	GT422	Midvaal	Midvaal, Gauteng	2011	1722.48000000000002	district	DC42	Gauteng	GT	B
173	municipality	KZN216	Hibiscus Coast	Hibiscus Coast, KwaZulu-Natal	2011	839.018000000000029	district	DC21	KwaZulu-Natal	KZN	B
174	municipality	KZN227	Richmond	Richmond, KwaZulu-Natal	2011	1255.59999999999991	district	DC22	KwaZulu-Natal	KZN	B
175	municipality	KZN241	Endumeni	Endumeni, KwaZulu-Natal	2011	1610.23000000000002	district	DC24	KwaZulu-Natal	KZN	B
176	municipality	KZN253	Emadlangeni	Emadlangeni, KwaZulu-Natal	2011	3539.32000000000016	district	DC25	KwaZulu-Natal	KZN	B
177	municipality	KZN271	Umhlabuyalingana	Umhlabuyalingana, KwaZulu-Natal	2011	4401.60999999999967	district	DC27	KwaZulu-Natal	KZN	B
178	municipality	KZN282	uMhlathuze	uMhlathuze, KwaZulu-Natal	2011	793.174999999999955	district	DC28	KwaZulu-Natal	KZN	B
179	municipality	KZN292	KwaDukuza	KwaDukuza, KwaZulu-Natal	2011	734.977999999999952	district	DC29	KwaZulu-Natal	KZN	B
180	municipality	KZN433	Greater Kokstad	Greater Kokstad, KwaZulu-Natal	2011	2679.82000000000016	district	DC43	KwaZulu-Natal	KZN	B
181	municipality	LIM334	Ba-Phalaborwa	Ba-Phalaborwa, Limpopo	2011	7461.64999999999964	district	DC33	Limpopo	LIM	B
182	municipality	LIM352	Aganang	Aganang, Limpopo	2011	1880.56999999999994	district	DC35	Limpopo	LIM	B
183	municipality	LIM364	Mookgopong	Mookgopong, Limpopo	2011	5688.85000000000036	district	DC36	Limpopo	LIM	B
184	municipality	LIM367	Mogalakwena	Mogalakwena, Limpopo	2011	6166.0600000000004	district	DC36	Limpopo	LIM	B
185	municipality	LIM471	Ephraim Mogale	Ephraim Mogale, Limpopo	2011	2011.30999999999995	district	DC47	Limpopo	LIM	B
186	municipality	LIM472	Elias Motsoaledi	Elias Motsoaledi, Limpopo	2011	3713.32999999999993	district	DC47	Limpopo	LIM	B
187	municipality	LIM473	Makhuduthamaga	Makhuduthamaga, Limpopo	2011	2096.59999999999991	district	DC47	Limpopo	LIM	B
188	municipality	LIM474	Fetakgomo	Fetakgomo, Limpopo	2011	1104.52999999999997	district	DC47	Limpopo	LIM	B
189	municipality	LIM475	Greater Tubatse	Greater Tubatse, Limpopo	2011	4601.96000000000004	district	DC47	Limpopo	LIM	B
190	municipality	MP301	Albert Luthuli	Albert Luthuli, Mpumalanga	2011	5559.39999999999964	district	DC30	Mpumalanga	MP	B
191	municipality	MP302	Msukaligwa	Msukaligwa, Mpumalanga	2011	6015.67000000000007	district	DC30	Mpumalanga	MP	B
192	municipality	MP304	Pixley Ka Seme	Pixley Ka Seme, Mpumalanga	2011	5227.21000000000004	district	DC30	Mpumalanga	MP	B
193	municipality	MP305	Lekwa	Lekwa, Mpumalanga	2011	4585.1899999999996	district	DC30	Mpumalanga	MP	B
194	municipality	MP306	Dipaleseng	Dipaleseng, Mpumalanga	2011	2616.55999999999995	district	DC30	Mpumalanga	MP	B
195	municipality	MP307	Govan Mbeki	Govan Mbeki, Mpumalanga	2011	2954.69000000000005	district	DC30	Mpumalanga	MP	B
196	municipality	MP312	Emalahleni	Emalahleni, Mpumalanga	2011	2677.61000000000013	district	DC31	Mpumalanga	MP	B
197	municipality	MP313	Steve Tshwete	Steve Tshwete, Mpumalanga	2011	3976.44999999999982	district	DC31	Mpumalanga	MP	B
198	municipality	MP314	Emakhazeni	Emakhazeni, Mpumalanga	2011	4735.57999999999993	district	DC31	Mpumalanga	MP	B
199	municipality	MP315	Thembisile	Thembisile, Mpumalanga	2011	2384.36999999999989	district	DC31	Mpumalanga	MP	B
200	municipality	MP316	Dr JS Moroka	Dr JS Moroka, Mpumalanga	2011	1416.47000000000003	district	DC31	Mpumalanga	MP	B
201	municipality	MP321	Thaba Chweu	Thaba Chweu, Mpumalanga	2011	5719.06999999999971	district	DC32	Mpumalanga	MP	B
202	municipality	MP323	Umjindi	Umjindi, Mpumalanga	2011	1745.38000000000011	district	DC32	Mpumalanga	MP	B
203	municipality	MP324	Nkomazi	Nkomazi, Mpumalanga	2011	4786.97000000000025	district	DC32	Mpumalanga	MP	B
205	municipality	NW371	Moretele	Moretele, North West	2011	1378.74000000000001	district	DC37	North West	NW	B
206	municipality	NW372	Madibeng	Madibeng, North West	2011	3839.21000000000004	district	DC37	North West	NW	B
207	municipality	NW374	Kgetlengrivier	Kgetlengrivier, North West	2011	3973.11999999999989	district	DC37	North West	NW	B
208	municipality	NW375	Moses Kotane	Moses Kotane, North West	2011	5719.06999999999971	district	DC37	North West	NW	B
209	municipality	NW381	Ratlou	Ratlou, North West	2011	4883.64999999999964	district	DC38	North West	NW	B
210	municipality	NW382	Tswaing	Tswaing, North West	2011	5966.25	district	DC38	North West	NW	B
211	municipality	NW383	Mafikeng	Mafikeng, North West	2011	3698.44000000000005	district	DC38	North West	NW	B
212	municipality	NW385	Ramotshere Moiloa	Ramotshere Moiloa, North West	2011	7192.88000000000011	district	DC38	North West	NW	B
213	municipality	NW392	Naledi	Naledi, North West	2011	6941.1899999999996	district	DC39	North West	NW	B
214	municipality	NW393	Mamusa	Mamusa, North West	2011	3614.84000000000015	district	DC39	North West	NW	B
215	municipality	NW394	Greater Taung	Greater Taung, North West	2011	5635.47000000000025	district	DC39	North West	NW	B
216	municipality	NW397	Kagisano/Molopo	Kagisano/Molopo, North West	2011	23827.2999999999993	district	DC39	North West	NW	B
217	municipality	NW401	Ventersdorp	Ventersdorp, North West	2011	3764.05000000000018	district	DC40	North West	NW	B
218	municipality	NW402	Tlokwe City Council	Tlokwe City Council, North West	2011	2673.67999999999984	district	DC40	North West	NW	B
219	municipality	NW403	City of Matlosana	City of Matlosana, North West	2011	3561.46000000000004	district	DC40	North West	NW	B
220	municipality	NW404	Maquassi Hills	Maquassi Hills, North West	2011	4643.05000000000018	district	DC40	North West	NW	B
221	municipality	NC061	Richtersveld	Richtersveld, Northern Cape	2011	9607.68000000000029	district	DC6	Northern Cape	NC	B
222	municipality	NC064	Kamiesberg	Kamiesberg, Northern Cape	2011	14210.2000000000007	district	DC6	Northern Cape	NC	B
223	municipality	NC065	Hantam	Hantam, Northern Cape	2011	36128.0999999999985	district	DC6	Northern Cape	NC	B
224	municipality	NC066	Karoo Hoogland	Karoo Hoogland, Northern Cape	2011	32273.9000000000015	district	DC6	Northern Cape	NC	B
166	municipality	MAN	Mangaung	Mangaung, Free State	2011	6283.98999999999978	province	FS	Free State	FS	A
264	municipality	MP303	Mkhondo	Mkhondo, Mpumalanga	2011	4882.17000000000007	district	DC30	Mpumalanga	MP	B
265	municipality	MP311	Victor Khanye	Victor Khanye, Mpumalanga	2011	1567.76999999999998	district	DC31	Mpumalanga	MP	B
266	municipality	MP322	Mbombela	Mbombela, Mpumalanga	2011	5394.43000000000029	district	DC32	Mpumalanga	MP	B
267	municipality	NW373	Rustenburg	Rustenburg, North West	2011	3423.26000000000022	district	DC37	North West	NW	B
268	municipality	NW384	Ditsobotla	Ditsobotla, North West	2011	6464.86999999999989	district	DC38	North West	NW	B
269	municipality	NW396	Lekwa-Teemane	Lekwa-Teemane, North West	2011	3681.19999999999982	district	DC39	North West	NW	B
270	municipality	NC062	Nama Khoi	Nama Khoi, Northern Cape	2011	17988.5999999999985	district	DC6	Northern Cape	NC	B
225	municipality	NC067	Khâi-Ma	Khâi-Ma, Northern Cape	2011	16627.9000000000015	district	DC6	Northern Cape	NC	B
271	municipality	NC071	Ubuntu	Ubuntu, Northern Cape	2011	20389.2000000000007	district	DC7	Northern Cape	NC	B
226	municipality	NC072	Umsobomvu	Umsobomvu, Northern Cape	2011	6818.52000000000044	district	DC7	Northern Cape	NC	B
227	municipality	NC073	Emthanjeni	Emthanjeni, Northern Cape	2011	13472.2999999999993	district	DC7	Northern Cape	NC	B
228	municipality	NC074	Kareeberg	Kareeberg, Northern Cape	2011	17702	district	DC7	Northern Cape	NC	B
229	municipality	NC075	Renosterberg	Renosterberg, Northern Cape	2011	5527.14999999999964	district	DC7	Northern Cape	NC	B
230	municipality	NC076	Thembelihle	Thembelihle, Northern Cape	2011	8023.06999999999971	district	DC7	Northern Cape	NC	B
272	municipality	NC077	Siyathemba	Siyathemba, Northern Cape	2011	14724.7999999999993	district	DC7	Northern Cape	NC	B
231	municipality	NC078	Siyancuma	Siyancuma, Northern Cape	2011	16752.7999999999993	district	DC7	Northern Cape	NC	B
232	municipality	NC081	Mier	Mier, Northern Cape	2011	22468.4000000000015	district	DC8	Northern Cape	NC	B
233	municipality	NC082	Kai !Garib	Kai !Garib, Northern Cape	2011	26358	district	DC8	Northern Cape	NC	B
234	municipality	NC083	//Khara Hais	//Khara Hais, Northern Cape	2011	21779.7999999999993	district	DC8	Northern Cape	NC	B
235	municipality	NC084	!Kheis	!Kheis, Northern Cape	2011	11107.5	district	DC8	Northern Cape	NC	B
273	municipality	NC085	Tsantsabane	Tsantsabane, Northern Cape	2011	18332.7999999999993	district	DC8	Northern Cape	NC	B
236	municipality	NC086	Kgatelopele	Kgatelopele, Northern Cape	2011	2477.92999999999984	district	DC8	Northern Cape	NC	B
237	municipality	NC091	Sol Plaatjie	Sol Plaatjie, Northern Cape	2011	3145.38999999999987	district	DC9	Northern Cape	NC	B
238	municipality	NC092	Dikgatlong	Dikgatlong, Northern Cape	2011	7314.72000000000025	district	DC9	Northern Cape	NC	B
239	municipality	NC093	Magareng	Magareng, Northern Cape	2011	1541.67000000000007	district	DC9	Northern Cape	NC	B
274	municipality	NC094	Phokwane	Phokwane, Northern Cape	2011	833.875	district	DC9	Northern Cape	NC	B
240	municipality	NC451	Joe Morolong	Joe Morolong, Northern Cape	2011	20172	district	DC45	Northern Cape	NC	B
241	municipality	NC452	Ga-Segonyana	Ga-Segonyana, Northern Cape	2011	4491.64000000000033	district	DC45	Northern Cape	NC	B
242	municipality	NC453	Gamagara	Gamagara, Northern Cape	2011	2619.42000000000007	district	DC45	Northern Cape	NC	B
244	municipality	WC011	Matzikama	Matzikama, Western Cape	2011	12981.3999999999996	district	DC1	Western Cape	WC	B
275	municipality	WC012	Cederberg	Cederberg, Western Cape	2011	8007.47000000000025	district	DC1	Western Cape	WC	B
245	municipality	WC013	Bergrivier	Bergrivier, Western Cape	2011	4407.03999999999996	district	DC1	Western Cape	WC	B
246	municipality	WC014	Saldanha Bay	Saldanha Bay, Western Cape	2011	2015.36999999999989	district	DC1	Western Cape	WC	B
247	municipality	WC015	Swartland	Swartland, Western Cape	2011	3712.5300000000002	district	DC1	Western Cape	WC	B
248	municipality	WC022	Witzenberg	Witzenberg, Western Cape	2011	10752.7000000000007	district	DC2	Western Cape	WC	B
249	municipality	WC023	Drakenstein	Drakenstein, Western Cape	2011	1537.66000000000008	district	DC2	Western Cape	WC	B
276	municipality	WC024	Stellenbosch	Stellenbosch, Western Cape	2011	831.044999999999959	district	DC2	Western Cape	WC	B
250	municipality	WC025	Breede Valley	Breede Valley, Western Cape	2011	3833.51999999999998	district	DC2	Western Cape	WC	B
251	municipality	WC026	Langeberg	Langeberg, Western Cape	2011	4517.69999999999982	district	DC2	Western Cape	WC	B
252	municipality	WC031	Theewaterskloof	Theewaterskloof, Western Cape	2011	3231.63999999999987	district	DC3	Western Cape	WC	B
253	municipality	WC032	Overstrand	Overstrand, Western Cape	2011	1707.50999999999999	district	DC3	Western Cape	WC	B
277	municipality	WC033	Cape Agulhas	Cape Agulhas, Western Cape	2011	3466.59999999999991	district	DC3	Western Cape	WC	B
254	municipality	WC034	Swellendam	Swellendam, Western Cape	2011	3835.09000000000015	district	DC3	Western Cape	WC	B
255	municipality	WC041	Kannaland	Kannaland, Western Cape	2011	4758.07999999999993	district	DC4	Western Cape	WC	B
256	municipality	WC042	Hessequa	Hessequa, Western Cape	2011	5733.48999999999978	district	DC4	Western Cape	WC	B
257	municipality	WC043	Mossel Bay	Mossel Bay, Western Cape	2011	2010.82999999999993	district	DC4	Western Cape	WC	B
258	municipality	WC044	George	George, Western Cape	2011	5191.01000000000022	district	DC4	Western Cape	WC	B
278	municipality	WC045	Oudtshoorn	Oudtshoorn, Western Cape	2011	3537.07000000000016	district	DC4	Western Cape	WC	B
259	municipality	WC047	Bitou	Bitou, Western Cape	2011	991.860000000000014	district	DC4	Western Cape	WC	B
260	municipality	WC048	Knysna	Knysna, Western Cape	2011	1108.76999999999998	district	DC4	Western Cape	WC	B
261	municipality	WC051	Laingsburg	Laingsburg, Western Cape	2011	8784.47999999999956	district	DC5	Western Cape	WC	B
262	municipality	WC052	Prince Albert	Prince Albert, Western Cape	2011	8152.90999999999985	district	DC5	Western Cape	WC	B
263	municipality	WC053	Beaufort West	Beaufort West, Western Cape	2011	21916.5999999999985	district	DC5	Western Cape	WC	B
243	municipality	CPT	City of Cape Town	City of Cape Town, Western Cape	2011	2439.7800000000002	province	WC	Western Cape	WC	A
\.


--
-- Name: scorecard_geography_id_seq; Type: SEQUENCE SET; Schema: public; Owner: municipal_finance
--

SELECT pg_catalog.setval('scorecard_geography_id_seq', 278, true);


--
-- Name: scorecard_geography_geo_level_1b28c178_uniq; Type: CONSTRAINT; Schema: public; Owner: municipal_finance; Tablespace: 
--

ALTER TABLE ONLY scorecard_geography
    ADD CONSTRAINT scorecard_geography_geo_level_1b28c178_uniq UNIQUE (geo_level, geo_code);


--
-- Name: scorecard_geography_pkey; Type: CONSTRAINT; Schema: public; Owner: municipal_finance; Tablespace: 
--

ALTER TABLE ONLY scorecard_geography
    ADD CONSTRAINT scorecard_geography_pkey PRIMARY KEY (id);


--
-- Name: scorecard_geography_2fc6351a; Type: INDEX; Schema: public; Owner: municipal_finance; Tablespace: 
--

CREATE INDEX scorecard_geography_2fc6351a ON scorecard_geography USING btree (long_name);


--
-- Name: scorecard_geography_84cdc76c; Type: INDEX; Schema: public; Owner: municipal_finance; Tablespace: 
--

CREATE INDEX scorecard_geography_84cdc76c ON scorecard_geography USING btree (year);


--
-- Name: scorecard_geography_b068931c; Type: INDEX; Schema: public; Owner: municipal_finance; Tablespace: 
--

CREATE INDEX scorecard_geography_b068931c ON scorecard_geography USING btree (name);


--
-- Name: scorecard_geography_long_name_d5fe0964_like; Type: INDEX; Schema: public; Owner: municipal_finance; Tablespace: 
--

CREATE INDEX scorecard_geography_long_name_d5fe0964_like ON scorecard_geography USING btree (long_name varchar_pattern_ops);


--
-- Name: scorecard_geography_name_52e408f6_like; Type: INDEX; Schema: public; Owner: municipal_finance; Tablespace: 
--

CREATE INDEX scorecard_geography_name_52e408f6_like ON scorecard_geography USING btree (name varchar_pattern_ops);


--
-- PostgreSQL database dump complete
--

