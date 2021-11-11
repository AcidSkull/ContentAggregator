--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: linuxiac; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.linuxiac (
    id integer NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.linuxiac OWNER TO postgres;

--
-- Name: linuxiac_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.linuxiac_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.linuxiac_id_seq OWNER TO postgres;

--
-- Name: linuxiac_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.linuxiac_id_seq OWNED BY public.linuxiac.id;


--
-- Name: axios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.axios (
    id integer DEFAULT nextval('public.linuxiac_id_seq'::regclass) NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.axios OWNER TO postgres;

--
-- Name: cnet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cnet (
    id integer DEFAULT nextval('public.linuxiac_id_seq'::regclass) NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.cnet OWNER TO postgres;

--
-- Name: digg; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.digg (
    id integer DEFAULT nextval('public.linuxiac_id_seq'::regclass) NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.digg OWNER TO postgres;

--
-- Name: eff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eff (
    id integer DEFAULT nextval('public.linuxiac_id_seq'::regclass) NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.eff OWNER TO postgres;

--
-- Name: itsfoss; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itsfoss (
    id integer DEFAULT nextval('public.linuxiac_id_seq'::regclass) NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.itsfoss OWNER TO postgres;

--
-- Name: techradar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.techradar (
    id integer DEFAULT nextval('public.linuxiac_id_seq'::regclass) NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.techradar OWNER TO postgres;

--
-- Name: thenextweb; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.thenextweb (
    id integer DEFAULT nextval('public.linuxiac_id_seq'::regclass) NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.thenextweb OWNER TO postgres;

--
-- Name: wired; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wired (
    id integer DEFAULT nextval('public.linuxiac_id_seq'::regclass) NOT NULL,
    title text,
    anchor text
);


ALTER TABLE public.wired OWNER TO postgres;

--
-- Name: linuxiac id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.linuxiac ALTER COLUMN id SET DEFAULT nextval('public.linuxiac_id_seq'::regclass);


--
-- Name: axios axios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.axios
    ADD CONSTRAINT axios_pkey PRIMARY KEY (id);


--
-- Name: cnet cnet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cnet
    ADD CONSTRAINT cnet_pkey PRIMARY KEY (id);


--
-- Name: digg digg_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digg
    ADD CONSTRAINT digg_pkey PRIMARY KEY (id);


--
-- Name: eff eff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.eff
    ADD CONSTRAINT eff_pkey PRIMARY KEY (id);


--
-- Name: itsfoss itsfoss_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itsfoss
    ADD CONSTRAINT itsfoss_pkey PRIMARY KEY (id);


--
-- Name: linuxiac linuxiac_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.linuxiac
    ADD CONSTRAINT linuxiac_pkey PRIMARY KEY (id);


--
-- Name: techradar techradar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.techradar
    ADD CONSTRAINT techradar_pkey PRIMARY KEY (id);


--
-- Name: thenextweb thenextweb_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thenextweb
    ADD CONSTRAINT thenextweb_pkey PRIMARY KEY (id);


--
-- Name: wired wired_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wired
    ADD CONSTRAINT wired_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

