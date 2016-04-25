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

DROP INDEX IF EXISTS public.wazimap_geography_name_36b79089_like;
DROP INDEX IF EXISTS public.wazimap_geography_b068931c;
DROP INDEX IF EXISTS public.wazimap_geography_84cdc76c;
DROP INDEX IF EXISTS public.wazimap_geography_2fc6351a;
ALTER TABLE IF EXISTS ONLY public.wazimap_geography DROP CONSTRAINT IF EXISTS wazimap_geography_pkey;
ALTER TABLE IF EXISTS ONLY public.wazimap_geography DROP CONSTRAINT IF EXISTS wazimap_geography_geo_level_9a5128d2_uniq;
ALTER TABLE IF EXISTS public.wazimap_geography ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.wazimap_geography_id_seq;
DROP TABLE IF EXISTS public.wazimap_geography;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: wazimap_geography; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE wazimap_geography (
    id integer NOT NULL,
    geo_level character varying(15) NOT NULL,
    geo_code character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    year integer,
    square_kms double precision,
    parent_level character varying(15),
    parent_code character varying(10),
    long_name character varying(100)
);


--
-- Name: wazimap_geography_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE wazimap_geography_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: wazimap_geography_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE wazimap_geography_id_seq OWNED BY wazimap_geography.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY wazimap_geography ALTER COLUMN id SET DEFAULT nextval('wazimap_geography_id_seq'::regclass);


--
-- Data for Name: wazimap_geography; Type: TABLE DATA; Schema: public; Owner: -
--

COPY wazimap_geography (id, geo_level, geo_code, name, year, square_kms, parent_level, parent_code, long_name) FROM stdin;
4743	district	DC1	West Coast	2011	3130.12417700000015	province	WC	West Coast, Western Cape
4744	district	DC10	Cacadu	2011	5856.077988	province	EC	Cacadu, Eastern Cape
4745	district	DC12	Amathole	2011	2171.73260900000014	province	EC	Amathole, Eastern Cape
4746	district	DC13	Chris Hani	2011	3636.02271599999995	province	EC	Chris Hani, Eastern Cape
4747	district	DC14	Joe Gqabi	2011	2582.56499699999995	province	EC	Joe Gqabi, Eastern Cape
4748	district	DC15	O.R.Tambo	2011	1216.96672100000001	province	EC	O.R.Tambo, Eastern Cape
4749	district	DC16	Xhariep	2011	3793.00496699999985	province	FS	Xhariep, Free State
4750	district	DC18	Lejweleputswa	2011	3216.80298399999992	province	FS	Lejweleputswa, Free State
4751	district	DC19	Thabo Mofutsanyane	2011	3351.68450200000007	province	FS	Thabo Mofutsanyane, Free State
4752	district	DC2	Cape Winelands	2011	2158.7342749999998	province	WC	Cape Winelands, Western Cape
4753	district	DC20	Fezile Dabi	2011	2082.91201499999988	province	FS	Fezile Dabi, Free State
4754	district	DC21	Ugu	2011	5079.76948100000027	province	KZN	Ugu, KwaZulu-Natal
4755	district	DC22	Umgungundlovu	2011	9578.93650499999967	province	KZN	Umgungundlovu, KwaZulu-Natal
4756	district	DC23	Uthukela	2011	1140.83048099999996	province	KZN	Uthukela, KwaZulu-Natal
4757	district	DC24	Umzinyathi	2011	8651.94117499999993	province	KZN	Umzinyathi, KwaZulu-Natal
4758	district	DC25	Amajuba	2011	6963.33322099999987	province	KZN	Amajuba, KwaZulu-Natal
4759	district	DC26	Zululand	2011	1491.16610300000002	province	KZN	Zululand, KwaZulu-Natal
4760	district	DC27	Umkhanyakude	2011	1396.18629099999998	province	KZN	Umkhanyakude, KwaZulu-Natal
4761	district	DC28	Uthungulu	2011	8273.05495800000062	province	KZN	Uthungulu, KwaZulu-Natal
4762	district	DC29	iLembe	2011	3292.25921299999982	province	KZN	iLembe, KwaZulu-Natal
4763	district	DC3	Overberg	2011	1230.11331100000007	province	WC	Overberg, Western Cape
4764	district	DC30	Gert Sibande	2011	3209.72732200000019	province	MP	Gert Sibande, Mpumalanga
4765	district	DC31	Nkangala	2011	1689.92186500000003	province	MP	Nkangala, Mpumalanga
4766	district	DC32	Ehlanzeni	2011	2813.69942399999991	province	MP	Ehlanzeni, Mpumalanga
4767	district	DC33	Mopani	2011	2019.33166699999992	province	LIM	Mopani, Limpopo
4768	district	DC34	Vhembe	2011	2583.89159299999983	province	LIM	Vhembe, Limpopo
4769	district	DC35	Capricorn	2011	2190.53465199999982	province	LIM	Capricorn, Limpopo
4770	district	DC36	Waterberg	2011	4531.56430699999964	province	LIM	Waterberg, Limpopo
4771	district	DC37	Bojanala	2011	1848.95336300000008	province	NW	Bojanala, North West
4772	district	DC38	Ngaka Modiri Molema	2011	2844.07866800000011	province	NW	Ngaka Modiri Molema, North West
4773	district	DC39	Dr Ruth Segomotsi Mompati	2011	4405.23903799999971	province	NW	Dr Ruth Segomotsi Mompati, North West
4774	district	DC4	Eden	2011	2345.06392499999993	province	WC	Eden, Western Cape
4775	district	DC40	Dr Kenneth Kaunda	2011	1475.93892000000005	province	NW	Dr Kenneth Kaunda, North West
4776	district	DC42	Sedibeng	2011	4206.52779100000043	province	GT	Sedibeng, Gauteng
4777	district	DC43	Sisonke	2011	1061.80334799999991	province	KZN	Sisonke, KwaZulu-Natal
4778	district	DC44	Alfred Nzo	2011	1080.05921199999989	province	EC	Alfred Nzo, Eastern Cape
4779	district	DC45	John Taolo Gaetsewe	2011	2749.89137100000016	province	NC	John Taolo Gaetsewe, Northern Cape
4780	district	DC47	Sekhukhune	2011	1364.58807499999989	province	LIM	Sekhukhune, Limpopo
4781	district	DC48	West Rand	2011	4120.99300399999993	province	GT	West Rand, Gauteng
4782	district	DC5	Central Karoo	2011	3907.3087129999999	province	WC	Central Karoo, Western Cape
4783	district	DC6	Namakwa	2011	1276.63268599999992	province	NC	Namakwa, Northern Cape
4784	district	DC7	Pixley ka Seme	2011	1040.94585400000005	province	NC	Pixley ka Seme, Northern Cape
4785	district	DC8	Siyanda	2011	1032.97298099999989	province	NC	Siyanda, Northern Cape
4786	district	DC9	Frances Baard	2011	1293.09347200000002	province	NC	Frances Baard, Northern Cape
4422	municipality	EC442	Umzimvubu	2011	2577.23000000000002	province	EC	Umzimvubu, Eastern Cape
4423	municipality	EC443	Mbizana	2011	2416.7199999999998	province	EC	Mbizana, Eastern Cape
4424	municipality	EC444	Ntabankulu	2011	1384.96000000000004	province	EC	Ntabankulu, Eastern Cape
4425	municipality	FS161	Letsemeng	2011	9828.57999999999993	province	FS	Letsemeng, Free State
4426	municipality	FS162	Kopanong	2011	15645.1000000000004	province	FS	Kopanong, Free State
4427	municipality	FS163	Mohokare	2011	8775.97999999999956	province	FS	Mohokare, Free State
4418	municipality	EC154	Port St Johns	2011	1291.20000000000005	province	EC	Port St Johns, Eastern Cape
4419	municipality	EC155	Nyandeni	2011	2474.01000000000022	province	EC	Nyandeni, Eastern Cape
4428	municipality	FS181	Masilonyana	2011	6796.09000000000015	province	FS	Masilonyana, Free State
4429	municipality	FS182	Tokologo	2011	9325.86000000000058	province	FS	Tokologo, Free State
4430	municipality	FS183	Tswelopele	2011	6524.06999999999971	province	FS	Tswelopele, Free State
4395	municipality	EC102	Blue Crane Route	2011	11068.6000000000004	province	EC	Blue Crane Route, Eastern Cape
4396	municipality	EC103	Ikwezi	2011	4562.72999999999956	province	EC	Ikwezi, Eastern Cape
4397	municipality	EC104	Makana	2011	4375.63000000000011	province	EC	Makana, Eastern Cape
4398	municipality	EC106	Sundays River Valley	2011	5993.52000000000044	province	EC	Sundays River Valley, Eastern Cape
4399	municipality	EC107	Baviaans	2011	11668.2999999999993	province	EC	Baviaans, Eastern Cape
4400	municipality	EC108	Kouga	2011	2669.82000000000016	province	EC	Kouga, Eastern Cape
4401	municipality	EC109	Kou-Kamma	2011	3642.01999999999998	province	EC	Kou-Kamma, Eastern Cape
4402	municipality	EC121	Mbhashe	2011	3169.44999999999982	province	EC	Mbhashe, Eastern Cape
4403	municipality	EC123	Great Kei	2011	1735.99000000000001	province	EC	Great Kei, Eastern Cape
4404	municipality	EC124	Amahlathi	2011	4820.22000000000025	province	EC	Amahlathi, Eastern Cape
4405	municipality	EC126	Ngqushwa	2011	2240.90999999999985	province	EC	Ngqushwa, Eastern Cape
4406	municipality	EC127	Nkonkobe	2011	3626.17999999999984	province	EC	Nkonkobe, Eastern Cape
4407	municipality	EC131	Inxuba Yethemba	2011	11662.7000000000007	province	EC	Inxuba Yethemba, Eastern Cape
4408	municipality	EC132	Tsolwana	2011	6086.81999999999971	province	EC	Tsolwana, Eastern Cape
4409	municipality	EC133	Inkwanca	2011	3584.23999999999978	province	EC	Inkwanca, Eastern Cape
4410	municipality	EC134	Lukanji	2011	3812.86000000000013	province	EC	Lukanji, Eastern Cape
4411	municipality	EC136	Emalahleni	2011	3447.19999999999982	province	EC	Emalahleni, Eastern Cape
4412	municipality	EC137	Engcobo	2011	2483.86999999999989	province	EC	Engcobo, Eastern Cape
4413	municipality	EC138	Sakhisizwe	2011	2354.7199999999998	province	EC	Sakhisizwe, Eastern Cape
4414	municipality	EC141	Elundini	2011	5064.53999999999996	province	EC	Elundini, Eastern Cape
4415	municipality	EC142	Senqu	2011	7329.42000000000007	province	EC	Senqu, Eastern Cape
4416	municipality	EC143	Maletswai	2011	4357.64999999999964	province	EC	Maletswai, Eastern Cape
4417	municipality	EC153	Ngquza Hill	2011	2476.82999999999993	province	EC	Ngquza Hill, Eastern Cape
4420	municipality	EC156	Mhlontlo	2011	2826.09000000000015	province	EC	Mhlontlo, Eastern Cape
4421	municipality	EC441	Matatiele	2011	4352.3100000000004	province	EC	Matatiele, Eastern Cape
4431	municipality	FS184	Matjhabeng	2011	5155.46000000000004	province	FS	Matjhabeng, Free State
4432	municipality	FS185	Nala	2011	4128.80000000000018	province	FS	Nala, Free State
4433	municipality	FS192	Dihlabeng	2011	4879.96000000000004	province	FS	Dihlabeng, Free State
4434	municipality	FS193	Nketoana	2011	5611.11999999999989	province	FS	Nketoana, Free State
4435	municipality	FS194	Maluti a Phofung	2011	4337.67000000000007	province	FS	Maluti a Phofung, Free State
4436	municipality	FS195	Phumelela	2011	8183.43000000000029	province	FS	Phumelela, Free State
4437	municipality	FS201	Moqhaka	2011	7924.5600000000004	province	FS	Moqhaka, Free State
4438	municipality	FS203	Ngwathe	2011	7055.01000000000022	province	FS	Ngwathe, Free State
4439	municipality	FS204	Metsimaholo	2011	1717.09999999999991	province	FS	Metsimaholo, Free State
4440	municipality	FS205	Mafube	2011	3971.36000000000013	province	FS	Mafube, Free State
4441	municipality	GT421	Emfuleni	2011	965.894000000000005	province	GT	Emfuleni, Gauteng
4442	municipality	GT423	Lesedi	2011	1484.3900000000001	province	GT	Lesedi, Gauteng
4443	municipality	GT481	Mogale City	2011	1342.16000000000008	province	GT	Mogale City, Gauteng
4444	municipality	GT482	Randfontein	2011	474.894000000000005	province	GT	Randfontein, Gauteng
4445	municipality	GT483	Westonaria	2011	639.823999999999955	province	GT	Westonaria, Gauteng
4446	municipality	KZN211	Vulamehlo	2011	959.923999999999978	province	KZN	Vulamehlo, KwaZulu-Natal
4447	municipality	KZN212	Umdoni	2011	251.52600000000001	province	KZN	Umdoni, KwaZulu-Natal
4448	municipality	KZN213	Umzumbe	2011	1258.88000000000011	province	KZN	Umzumbe, KwaZulu-Natal
4449	municipality	KZN214	UMuziwabantu	2011	1089.47000000000003	province	KZN	UMuziwabantu, KwaZulu-Natal
4450	municipality	KZN215	Ezingoleni	2011	648.07000000000005	province	KZN	Ezingoleni, KwaZulu-Natal
4451	municipality	KZN221	uMshwathi	2011	1817.94000000000005	province	KZN	uMshwathi, KwaZulu-Natal
4452	municipality	KZN222	uMngeni	2011	1566.51999999999998	province	KZN	uMngeni, KwaZulu-Natal
4453	municipality	KZN223	Mpofana	2011	1819.78999999999996	province	KZN	Mpofana, KwaZulu-Natal
4454	municipality	KZN224	Impendle	2011	1528.19000000000005	province	KZN	Impendle, KwaZulu-Natal
4455	municipality	KZN225	The Msunduzi	2011	634.010999999999967	province	KZN	The Msunduzi, KwaZulu-Natal
4456	municipality	KZN226	Mkhambathini	2011	890.875999999999976	province	KZN	Mkhambathini, KwaZulu-Natal
4457	municipality	KZN232	Emnambithi/Ladysmith	2011	2964.84000000000015	province	KZN	Emnambithi/Ladysmith, KwaZulu-Natal
4458	municipality	KZN233	Indaka	2011	991.539999999999964	province	KZN	Indaka, KwaZulu-Natal
4459	municipality	KZN234	Umtshezi	2011	1972.45000000000005	province	KZN	Umtshezi, KwaZulu-Natal
4460	municipality	KZN235	Okhahlamba	2011	3970.98000000000002	province	KZN	Okhahlamba, KwaZulu-Natal
4461	municipality	KZN236	Imbabazane	2011	1426.30999999999995	province	KZN	Imbabazane, KwaZulu-Natal
4462	municipality	KZN242	Nqutu	2011	1962.25999999999999	province	KZN	Nqutu, KwaZulu-Natal
4463	municipality	KZN244	Msinga	2011	2501.13999999999987	province	KZN	Msinga, KwaZulu-Natal
4464	municipality	KZN245	Umvoti	2011	2515.5300000000002	province	KZN	Umvoti, KwaZulu-Natal
4465	municipality	KZN252	Newcastle	2011	1855.28999999999996	province	KZN	Newcastle, KwaZulu-Natal
4466	municipality	KZN254	Dannhauser	2011	1515.91000000000008	province	KZN	Dannhauser, KwaZulu-Natal
4467	municipality	KZN261	eDumbe	2011	1942.75999999999999	province	KZN	eDumbe, KwaZulu-Natal
4468	municipality	KZN262	UPhongolo	2011	3239.19000000000005	province	KZN	UPhongolo, KwaZulu-Natal
4469	municipality	KZN263	Abaqulusi	2011	4184.63000000000011	province	KZN	Abaqulusi, KwaZulu-Natal
4470	municipality	KZN265	Nongoma	2011	2182.11000000000013	province	KZN	Nongoma, KwaZulu-Natal
4471	municipality	KZN266	Ulundi	2011	3250.28999999999996	province	KZN	Ulundi, KwaZulu-Natal
4472	municipality	KZN272	Jozini	2011	3442.25	province	KZN	Jozini, KwaZulu-Natal
4473	municipality	KZN273	The Big 5 False Bay	2011	2486.53999999999996	province	KZN	The Big 5 False Bay, KwaZulu-Natal
4474	municipality	KZN274	Hlabisa	2011	1555.13000000000011	province	KZN	Hlabisa, KwaZulu-Natal
4475	municipality	KZN275	Mtubatuba	2011	1969.83999999999992	province	KZN	Mtubatuba, KwaZulu-Natal
4476	municipality	KZN281	Mfolozi	2011	1209.98000000000002	province	KZN	Mfolozi, KwaZulu-Natal
4477	municipality	KZN283	Ntambanana	2011	1082.75999999999999	province	KZN	Ntambanana, KwaZulu-Natal
4478	municipality	KZN284	uMlalazi	2011	2213.94000000000005	province	KZN	uMlalazi, KwaZulu-Natal
4479	municipality	KZN285	Mthonjaneni	2011	1085.97000000000003	province	KZN	Mthonjaneni, KwaZulu-Natal
4480	municipality	KZN286	Nkandla	2011	1827.57999999999993	province	KZN	Nkandla, KwaZulu-Natal
4481	municipality	KZN291	Mandeni	2011	545.480999999999995	province	KZN	Mandeni, KwaZulu-Natal
4482	municipality	KZN293	Ndwedwe	2011	1092.8900000000001	province	KZN	Ndwedwe, KwaZulu-Natal
4483	municipality	KZN294	Maphumulo	2011	895.908999999999992	province	KZN	Maphumulo, KwaZulu-Natal
4484	municipality	KZN431	Ingwe	2011	1976.20000000000005	province	KZN	Ingwe, KwaZulu-Natal
4485	municipality	KZN432	Kwa Sani	2011	1851.90000000000009	province	KZN	Kwa Sani, KwaZulu-Natal
4486	municipality	KZN434	Ubuhlebezwe	2011	1604.02999999999997	province	KZN	Ubuhlebezwe, KwaZulu-Natal
4487	municipality	KZN435	Umzimkhulu	2011	2435.4699999999998	province	KZN	Umzimkhulu, KwaZulu-Natal
4488	municipality	LIM331	Greater Giyani	2011	4171.60999999999967	province	LIM	Greater Giyani, Limpopo
4489	municipality	LIM332	Greater Letaba	2011	1890.8900000000001	province	LIM	Greater Letaba, Limpopo
4490	municipality	LIM333	Greater Tzaneen	2011	3242.57999999999993	province	LIM	Greater Tzaneen, Limpopo
4491	municipality	LIM335	Maruleng	2011	3244.30000000000018	province	LIM	Maruleng, Limpopo
4492	municipality	LIM341	Musina	2011	7576.82999999999993	province	LIM	Musina, Limpopo
4493	municipality	LIM342	Mutale	2011	3886.17000000000007	province	LIM	Mutale, Limpopo
4494	municipality	LIM343	Thulamela	2011	5834.25	province	LIM	Thulamela, Limpopo
4495	municipality	LIM344	Makhado	2011	8299.70000000000073	province	LIM	Makhado, Limpopo
4496	municipality	LIM351	Blouberg	2011	9248.1200000000008	province	LIM	Blouberg, Limpopo
4497	municipality	LIM353	Molemole	2011	3347.32999999999993	province	LIM	Molemole, Limpopo
4498	municipality	LIM354	Polokwane	2011	3765.98000000000002	province	LIM	Polokwane, Limpopo
4499	municipality	LIM355	Lepele-Nkumpi	2011	3463.44999999999982	province	LIM	Lepele-Nkumpi, Limpopo
4500	municipality	LIM361	Thabazimbi	2011	11190.1000000000004	province	LIM	Thabazimbi, Limpopo
4501	municipality	LIM362	Lephalale	2011	13784.2000000000007	province	LIM	Lephalale, Limpopo
4502	municipality	LIM365	Modimolle	2011	4677.94999999999982	province	LIM	Modimolle, Limpopo
4503	municipality	LIM366	Bela-Bela	2011	3406.19999999999982	province	LIM	Bela-Bela, Limpopo
4504	municipality	BUF	Buffalo City	2011	2535.92999999999984	province	EC	Buffalo City, Eastern Cape
4505	municipality	EC101	Camdeboo	2011	12422.1000000000004	province	EC	Camdeboo, Eastern Cape
4506	municipality	EC105	Ndlambe	2011	1840.63000000000011	province	EC	Ndlambe, Eastern Cape
4507	municipality	EC122	Mnquma	2011	3270.23999999999978	province	EC	Mnquma, Eastern Cape
4508	municipality	EC128	Nxuba	2011	2731.92000000000007	province	EC	Nxuba, Eastern Cape
4509	municipality	EC135	Intsika Yethu	2011	2711.13999999999987	province	EC	Intsika Yethu, Eastern Cape
4510	municipality	EC144	Gariep	2011	8911.05999999999949	province	EC	Gariep, Eastern Cape
4511	municipality	EC157	King Sabata Dalindyebo	2011	3027.36999999999989	province	EC	King Sabata Dalindyebo, Eastern Cape
4512	municipality	NMA	Nelson Mandela Bay	2011	1958.91000000000008	province	EC	Nelson Mandela Bay, Eastern Cape
4513	municipality	FS164	Naledi	2011	3424.05999999999995	province	FS	Naledi, Free State
4514	municipality	FS191	Setsoto	2011	5966.35999999999967	province	FS	Setsoto, Free State
4515	municipality	FS196	Mantsopa	2011	4290.59000000000015	province	FS	Mantsopa, Free State
4516	municipality	MAN	Mangaung	2011	6283.98999999999978	province	FS	Mangaung, Free State
4517	municipality	EKU	Ekurhuleni	2011	1975.25999999999999	province	GT	Ekurhuleni, Gauteng
4518	municipality	GT422	Midvaal	2011	1722.48000000000002	province	GT	Midvaal, Gauteng
4519	municipality	GT484	Merafong City	2011	1630.53999999999996	province	GT	Merafong City, Gauteng
4520	municipality	JHB	City of Johannesburg	2011	1644.98000000000002	province	GT	City of Johannesburg, Gauteng
4521	municipality	TSH	City of Tshwane	2011	6297.88000000000011	province	GT	City of Tshwane, Gauteng
4522	municipality	ETH	eThekwini	2011	2291.30999999999995	province	KZN	eThekwini, KwaZulu-Natal
4523	municipality	KZN216	Hibiscus Coast	2011	839.018000000000029	province	KZN	Hibiscus Coast, KwaZulu-Natal
4524	municipality	KZN227	Richmond	2011	1255.59999999999991	province	KZN	Richmond, KwaZulu-Natal
4525	municipality	KZN241	Endumeni	2011	1610.23000000000002	province	KZN	Endumeni, KwaZulu-Natal
4526	municipality	KZN253	Emadlangeni	2011	3539.32000000000016	province	KZN	Emadlangeni, KwaZulu-Natal
4527	municipality	KZN271	Umhlabuyalingana	2011	4401.60999999999967	province	KZN	Umhlabuyalingana, KwaZulu-Natal
4528	municipality	KZN282	uMhlathuze	2011	793.174999999999955	province	KZN	uMhlathuze, KwaZulu-Natal
4529	municipality	KZN292	KwaDukuza	2011	734.977999999999952	province	KZN	KwaDukuza, KwaZulu-Natal
4530	municipality	KZN433	Greater Kokstad	2011	2679.82000000000016	province	KZN	Greater Kokstad, KwaZulu-Natal
4531	municipality	LIM334	Ba-Phalaborwa	2011	7461.64999999999964	province	LIM	Ba-Phalaborwa, Limpopo
4532	municipality	LIM352	Aganang	2011	1880.56999999999994	province	LIM	Aganang, Limpopo
4533	municipality	LIM364	Mookgopong	2011	5688.85000000000036	province	LIM	Mookgopong, Limpopo
4534	municipality	LIM367	Mogalakwena	2011	6166.0600000000004	province	LIM	Mogalakwena, Limpopo
4535	municipality	LIM471	Ephraim Mogale	2011	2011.30999999999995	province	LIM	Ephraim Mogale, Limpopo
4536	municipality	LIM472	Elias Motsoaledi	2011	3713.32999999999993	province	LIM	Elias Motsoaledi, Limpopo
4537	municipality	LIM473	Makhuduthamaga	2011	2096.59999999999991	province	LIM	Makhuduthamaga, Limpopo
4538	municipality	LIM474	Fetakgomo	2011	1104.52999999999997	province	LIM	Fetakgomo, Limpopo
4539	municipality	LIM475	Greater Tubatse	2011	4601.96000000000004	province	LIM	Greater Tubatse, Limpopo
4540	municipality	MP301	Albert Luthuli	2011	5559.39999999999964	province	MP	Albert Luthuli, Mpumalanga
4541	municipality	MP302	Msukaligwa	2011	6015.67000000000007	province	MP	Msukaligwa, Mpumalanga
4542	municipality	MP304	Pixley Ka Seme	2011	5227.21000000000004	province	MP	Pixley Ka Seme, Mpumalanga
4543	municipality	MP305	Lekwa	2011	4585.1899999999996	province	MP	Lekwa, Mpumalanga
4544	municipality	MP306	Dipaleseng	2011	2616.55999999999995	province	MP	Dipaleseng, Mpumalanga
4545	municipality	MP307	Govan Mbeki	2011	2954.69000000000005	province	MP	Govan Mbeki, Mpumalanga
4546	municipality	MP312	Emalahleni	2011	2677.61000000000013	province	MP	Emalahleni, Mpumalanga
4547	municipality	MP313	Steve Tshwete	2011	3976.44999999999982	province	MP	Steve Tshwete, Mpumalanga
4548	municipality	MP314	Emakhazeni	2011	4735.57999999999993	province	MP	Emakhazeni, Mpumalanga
4549	municipality	MP315	Thembisile	2011	2384.36999999999989	province	MP	Thembisile, Mpumalanga
4550	municipality	MP316	Dr JS Moroka	2011	1416.47000000000003	province	MP	Dr JS Moroka, Mpumalanga
4551	municipality	MP321	Thaba Chweu	2011	5719.06999999999971	province	MP	Thaba Chweu, Mpumalanga
4552	municipality	MP323	Umjindi	2011	1745.38000000000011	province	MP	Umjindi, Mpumalanga
4553	municipality	MP324	Nkomazi	2011	4786.97000000000025	province	MP	Nkomazi, Mpumalanga
4554	municipality	MP325	Bushbuckridge	2011	10249.7000000000007	province	MP	Bushbuckridge, Mpumalanga
4555	municipality	NW371	Moretele	2011	1378.74000000000001	province	NW	Moretele, North West
4556	municipality	NW372	Madibeng	2011	3839.21000000000004	province	NW	Madibeng, North West
4557	municipality	NW374	Kgetlengrivier	2011	3973.11999999999989	province	NW	Kgetlengrivier, North West
4558	municipality	NW375	Moses Kotane	2011	5719.06999999999971	province	NW	Moses Kotane, North West
4559	municipality	NW381	Ratlou	2011	4883.64999999999964	province	NW	Ratlou, North West
4560	municipality	NW382	Tswaing	2011	5966.25	province	NW	Tswaing, North West
4561	municipality	NW383	Mafikeng	2011	3698.44000000000005	province	NW	Mafikeng, North West
4562	municipality	NW385	Ramotshere Moiloa	2011	7192.88000000000011	province	NW	Ramotshere Moiloa, North West
4563	municipality	NW392	Naledi	2011	6941.1899999999996	province	NW	Naledi, North West
4564	municipality	NW393	Mamusa	2011	3614.84000000000015	province	NW	Mamusa, North West
4565	municipality	NW394	Greater Taung	2011	5635.47000000000025	province	NW	Greater Taung, North West
4566	municipality	NW397	Kagisano/Molopo	2011	23827.2999999999993	province	NW	Kagisano/Molopo, North West
4567	municipality	NW401	Ventersdorp	2011	3764.05000000000018	province	NW	Ventersdorp, North West
4568	municipality	NW402	Tlokwe City Council	2011	2673.67999999999984	province	NW	Tlokwe City Council, North West
4569	municipality	NW403	City of Matlosana	2011	3561.46000000000004	province	NW	City of Matlosana, North West
4570	municipality	NW404	Maquassi Hills	2011	4643.05000000000018	province	NW	Maquassi Hills, North West
4571	municipality	NC061	Richtersveld	2011	9607.68000000000029	province	NC	Richtersveld, Northern Cape
4572	municipality	NC064	Kamiesberg	2011	14210.2000000000007	province	NC	Kamiesberg, Northern Cape
4573	municipality	NC065	Hantam	2011	36128.0999999999985	province	NC	Hantam, Northern Cape
4574	municipality	NC066	Karoo Hoogland	2011	32273.9000000000015	province	NC	Karoo Hoogland, Northern Cape
4575	municipality	NC067	Khâi-Ma	2011	16627.9000000000015	province	NC	Khâi-Ma, Northern Cape
4576	municipality	NC072	Umsobomvu	2011	6818.52000000000044	province	NC	Umsobomvu, Northern Cape
4577	municipality	NC073	Emthanjeni	2011	13472.2999999999993	province	NC	Emthanjeni, Northern Cape
4578	municipality	NC074	Kareeberg	2011	17702	province	NC	Kareeberg, Northern Cape
4579	municipality	NC075	Renosterberg	2011	5527.14999999999964	province	NC	Renosterberg, Northern Cape
4580	municipality	NC076	Thembelihle	2011	8023.06999999999971	province	NC	Thembelihle, Northern Cape
4581	municipality	NC078	Siyancuma	2011	16752.7999999999993	province	NC	Siyancuma, Northern Cape
4582	municipality	NC081	Mier	2011	22468.4000000000015	province	NC	Mier, Northern Cape
4583	municipality	NC082	Kai !Garib	2011	26358	province	NC	Kai !Garib, Northern Cape
4584	municipality	NC083	//Khara Hais	2011	21779.7999999999993	province	NC	//Khara Hais, Northern Cape
4585	municipality	NC084	!Kheis	2011	11107.5	province	NC	!Kheis, Northern Cape
4586	municipality	NC086	Kgatelopele	2011	2477.92999999999984	province	NC	Kgatelopele, Northern Cape
4587	municipality	NC091	Sol Plaatjie	2011	3145.38999999999987	province	NC	Sol Plaatjie, Northern Cape
4588	municipality	NC092	Dikgatlong	2011	7314.72000000000025	province	NC	Dikgatlong, Northern Cape
4589	municipality	NC093	Magareng	2011	1541.67000000000007	province	NC	Magareng, Northern Cape
4590	municipality	NC451	Joe Morolong	2011	20172	province	NC	Joe Morolong, Northern Cape
4591	municipality	NC452	Ga-Segonyana	2011	4491.64000000000033	province	NC	Ga-Segonyana, Northern Cape
4592	municipality	NC453	Gamagara	2011	2619.42000000000007	province	NC	Gamagara, Northern Cape
4593	municipality	CPT	City of Cape Town	2011	2439.7800000000002	province	WC	City of Cape Town, Western Cape
4594	municipality	WC011	Matzikama	2011	12981.3999999999996	province	WC	Matzikama, Western Cape
4595	municipality	WC013	Bergrivier	2011	4407.03999999999996	province	WC	Bergrivier, Western Cape
4596	municipality	WC014	Saldanha Bay	2011	2015.36999999999989	province	WC	Saldanha Bay, Western Cape
4597	municipality	WC015	Swartland	2011	3712.5300000000002	province	WC	Swartland, Western Cape
4598	municipality	WC022	Witzenberg	2011	10752.7000000000007	province	WC	Witzenberg, Western Cape
4599	municipality	WC023	Drakenstein	2011	1537.66000000000008	province	WC	Drakenstein, Western Cape
4600	municipality	WC025	Breede Valley	2011	3833.51999999999998	province	WC	Breede Valley, Western Cape
4601	municipality	WC026	Langeberg	2011	4517.69999999999982	province	WC	Langeberg, Western Cape
4602	municipality	WC031	Theewaterskloof	2011	3231.63999999999987	province	WC	Theewaterskloof, Western Cape
4603	municipality	WC032	Overstrand	2011	1707.50999999999999	province	WC	Overstrand, Western Cape
4604	municipality	WC034	Swellendam	2011	3835.09000000000015	province	WC	Swellendam, Western Cape
4605	municipality	WC041	Kannaland	2011	4758.07999999999993	province	WC	Kannaland, Western Cape
4606	municipality	WC042	Hessequa	2011	5733.48999999999978	province	WC	Hessequa, Western Cape
4607	municipality	WC043	Mossel Bay	2011	2010.82999999999993	province	WC	Mossel Bay, Western Cape
4608	municipality	WC044	George	2011	5191.01000000000022	province	WC	George, Western Cape
4609	municipality	WC047	Bitou	2011	991.860000000000014	province	WC	Bitou, Western Cape
4610	municipality	WC048	Knysna	2011	1108.76999999999998	province	WC	Knysna, Western Cape
4611	municipality	WC051	Laingsburg	2011	8784.47999999999956	province	WC	Laingsburg, Western Cape
4612	municipality	WC052	Prince Albert	2011	8152.90999999999985	province	WC	Prince Albert, Western Cape
4613	municipality	WC053	Beaufort West	2011	21916.5999999999985	province	WC	Beaufort West, Western Cape
4614	municipality	MP303	Mkhondo	2011	4882.17000000000007	province	MP	Mkhondo, Mpumalanga
4615	municipality	MP311	Victor Khanye	2011	1567.76999999999998	province	MP	Victor Khanye, Mpumalanga
4616	municipality	MP322	Mbombela	2011	5394.43000000000029	province	MP	Mbombela, Mpumalanga
4617	municipality	NW373	Rustenburg	2011	3423.26000000000022	province	NW	Rustenburg, North West
4618	municipality	NW384	Ditsobotla	2011	6464.86999999999989	province	NW	Ditsobotla, North West
4619	municipality	NW396	Lekwa-Teemane	2011	3681.19999999999982	province	NW	Lekwa-Teemane, North West
4620	municipality	NC062	Nama Khoi	2011	17988.5999999999985	province	NC	Nama Khoi, Northern Cape
4621	municipality	NC071	Ubuntu	2011	20389.2000000000007	province	NC	Ubuntu, Northern Cape
4622	municipality	NC077	Siyathemba	2011	14724.7999999999993	province	NC	Siyathemba, Northern Cape
4623	municipality	NC085	Tsantsabane	2011	18332.7999999999993	province	NC	Tsantsabane, Northern Cape
4624	municipality	NC094	Phokwane	2011	833.875	province	NC	Phokwane, Northern Cape
4625	municipality	WC012	Cederberg	2011	8007.47000000000025	province	WC	Cederberg, Western Cape
4626	municipality	WC024	Stellenbosch	2011	831.044999999999959	province	WC	Stellenbosch, Western Cape
4627	municipality	WC033	Cape Agulhas	2011	3466.59999999999991	province	WC	Cape Agulhas, Western Cape
4628	municipality	WC045	Oudtshoorn	2011	3537.07000000000016	province	WC	Oudtshoorn, Western Cape
4629	province	EC	Eastern Cape	2011	169309.834100000007	country	ZA	\N
4630	province	FS	Free State	2011	130011.486499999999	country	ZA	\N
4631	province	GT	Gauteng	2011	18182.4923000000017	country	ZA	\N
4632	province	KZN	KwaZulu-Natal	2011	94451.0197999999946	country	ZA	\N
4633	province	LIM	Limpopo	2011	125806.0524	country	ZA	\N
4634	province	MP	Mpumalanga	2011	76544.303899999999	country	ZA	\N
4635	province	NW	North West	2011	105238.131299999994	country	ZA	\N
4636	province	NC	Northern Cape	2011	378276.609699999972	country	ZA	\N
4637	province	WC	Western Cape	2011	131521.559100000013	country	ZA	\N
4638	country	ZA	South Africa	2011	1229341.48919999995	\N	\N	\N
\.


--
-- Name: wazimap_geography_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('wazimap_geography_id_seq', 4786, true);


--
-- Name: wazimap_geography_geo_level_9a5128d2_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY wazimap_geography
    ADD CONSTRAINT wazimap_geography_geo_level_9a5128d2_uniq UNIQUE (geo_level, geo_code);


--
-- Name: wazimap_geography_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY wazimap_geography
    ADD CONSTRAINT wazimap_geography_pkey PRIMARY KEY (id);


--
-- Name: wazimap_geography_2fc6351a; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX wazimap_geography_2fc6351a ON wazimap_geography USING btree (long_name);


--
-- Name: wazimap_geography_84cdc76c; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX wazimap_geography_84cdc76c ON wazimap_geography USING btree (year);


--
-- Name: wazimap_geography_b068931c; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX wazimap_geography_b068931c ON wazimap_geography USING btree (name);


--
-- Name: wazimap_geography_name_36b79089_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX wazimap_geography_name_36b79089_like ON wazimap_geography USING btree (name varchar_pattern_ops);


--
-- PostgreSQL database dump complete
--

