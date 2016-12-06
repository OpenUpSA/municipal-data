--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

ALTER TABLE IF EXISTS ONLY public.municipal_finance_demarcationchanges DROP CONSTRAINT IF EXISTS municipal_finance_demarcationchanges_pkey;
ALTER TABLE IF EXISTS public.municipal_finance_demarcationchanges ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.municipal_finance_demarcationchanges_id_seq;
DROP TABLE IF EXISTS public.municipal_finance_demarcationchanges;
SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: municipal_finance_demarcationchanges; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE municipal_finance_demarcationchanges (
    id integer NOT NULL,
    date date NOT NULL,
    old_code text NOT NULL,
    new_code text NOT NULL,
    old_code_transition text NOT NULL,
    new_code_transition text NOT NULL
);


--
-- Name: municipal_finance_demarcationchanges_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE municipal_finance_demarcationchanges_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: municipal_finance_demarcationchanges_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE municipal_finance_demarcationchanges_id_seq OWNED BY municipal_finance_demarcationchanges.id;


--
-- Name: municipal_finance_demarcationchanges id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY municipal_finance_demarcationchanges ALTER COLUMN id SET DEFAULT nextval('municipal_finance_demarcationchanges_id_seq'::regclass);


--
-- Data for Name: municipal_finance_demarcationchanges; Type: TABLE DATA; Schema: public; Owner: -
--

COPY municipal_finance_demarcationchanges (id, date, old_code, new_code, old_code_transition, new_code_transition) FROM stdin;
1	2016-08-03	EC103	EC101	disestablished	continue
2	2016-08-03	EC107	EC101	disestablished	continue
3	2016-08-03	EC127	EC129	disestablished	established
4	2016-08-03	EC128	EC129	disestablished	established
5	2016-08-03	EC132	EC139	disestablished	established
6	2016-08-03	EC133	EC139	disestablished	established
7	2016-08-03	EC134	EC139	disestablished	established
8	2016-08-03	EC143	EC145	disestablished	established
9	2016-08-03	EC144	EC145	disestablished	established
10	2016-08-03	FS164	MAN	disestablished	continue
11	2016-08-03	GT482	GT485	disestablished	established
12	2016-08-03	GT483	GT485	disestablished	established
13	2016-08-03	KZN211	KZN212	disestablished	continue
14	2016-08-03	KZN215	KZN216	disestablished	continue
15	2016-08-03	KZN234	KZN237	disestablished	established
16	2016-08-03	KZN236	KZN237	disestablished	established
17	2016-08-03	KZN232	KZN238	disestablished	established
18	2016-08-03	KZN233	KZN238	disestablished	established
19	2016-08-03	KZN274	KZN276	disestablished	established
20	2016-08-03	KZN273	KZN276	disestablished	established
21	2016-08-03	KZN283	KZN281	disestablished	continue
22	2016-08-03	KZN283	KZN282	disestablished	continue
23	2016-08-03	KZN283	KZN285	disestablished	continue
24	2016-08-03	KZN431	KZN436	disestablished	established
25	2016-08-03	KZN432	KZN436	disestablished	established
26	2016-08-03	LIM342	LIM341	disestablished	continue
27	2016-08-03	LIM342	LIM343	disestablished	continue
28	2016-08-03	LIM343	LIM345	continue	established
29	2016-08-03	LIM344	LIM345	continue	established
30	2016-08-03	LIM352	LIM351	disestablished	continue
31	2016-08-03	LIM352	LIM353	disestablished	continue
32	2016-08-03	LIM352	LIM354	disestablished	continue
33	2016-08-03	LIM364	LIM368	disestablished	established
34	2016-08-03	LIM365	LIM368	disestablished	established
35	2016-08-03	LIM474	LIM476	disestablished	established
36	2016-08-03	LIM475	LIM476	disestablished	established
37	2016-08-03	MP322	MP326	disestablished	established
38	2016-08-03	MP323	MP326	disestablished	established
39	2016-08-03	NC081	NC087	disestablished	established
40	2016-08-03	NC083	NC087	disestablished	established
41	2016-08-03	NW401	NW405	disestablished	established
42	2016-08-03	NW402	NW405	disestablished	established
\.


--
-- Name: municipal_finance_demarcationchanges_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('municipal_finance_demarcationchanges_id_seq', 42, true);


--
-- Name: municipal_finance_demarcationchanges municipal_finance_demarcationchanges_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY municipal_finance_demarcationchanges
    ADD CONSTRAINT municipal_finance_demarcationchanges_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

