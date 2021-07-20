--
-- PostgreSQL database dump
--
 -- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2
 -- Started on 2020-05-08 07:52:45
 --
-- TOC entry 204 (class 1259 OID 16731)
-- Name: attendee; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE PUBLIC.ATTENDEE (ID integer NOT NULL,
																															FIRST_NAME text NOT NULL,
																															LAST_NAME text NOT NULL,
																															CONFERENCE_ID integer NOT NULL,
																															JOB_POSITION text NOT NULL,
																															EMAIL text NOT NULL,
																															COMPANY text NOT NULL,
																															CITY text NOT NULL,
																															STATE text NOT NULL,
																															INTERESTS text, SUBMITTED_DATE TIMESTAMP WITH TIME ZONE NOT NULL,
																															COMMENTS text);

--
 -- TOC entry 205 (class 1259 OID 16744)
 -- Name: attendee_id_seq; Type: SEQUENCE; Schema: public; Owner: -
 --

ALTER TABLE PUBLIC.ATTENDEE
ALTER COLUMN ID ADD GENERATED ALWAYS AS IDENTITY
	(SEQUENCE NAME PUBLIC.ATTENDEE_ID_SEQ START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1);

--
 -- TOC entry 202 (class 1259 OID 16722)
 -- Name: conference; Type: TABLE; Schema: public; Owner: -
 --

CREATE TABLE PUBLIC.CONFERENCE (ID integer NOT NULL,
																																	NAME CHARACTER VARYING(100) NOT NULL,
																																	ACTIVE BIT(1) NOT NULL, date date NOT NULL,
																																	PRICE double precision NOT NULL,
																																	ADDRESS CHARACTER VARYING(300) NOT NULL);

--
 -- TOC entry 203 (class 1259 OID 16729)
 -- Name: conference_id_seq; Type: SEQUENCE; Schema: public; Owner: -
 --

ALTER TABLE PUBLIC.CONFERENCE
ALTER COLUMN ID ADD GENERATED ALWAYS AS IDENTITY
	(SEQUENCE NAME PUBLIC.CONFERENCE_ID_SEQ START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 99999 CACHE 1);

--
 -- TOC entry 206 (class 1259 OID 16746)
 -- Name: notification; Type: TABLE; Schema: public; Owner: -
 --

CREATE TABLE PUBLIC.NOTIFICATION (ID integer NOT NULL,
																																			STATUS text NOT NULL,
																																			MESSAGE text NOT NULL,
																																			SUBMITTED_DATE TIMESTAMP WITH TIME ZONE,
																																			COMPLETED_DATE TIMESTAMP WITH TIME ZONE,
																																			SUBJECT text NOT NULL);

--
 -- TOC entry 207 (class 1259 OID 16754)
 -- Name: notification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
 --

ALTER TABLE PUBLIC.NOTIFICATION
ALTER COLUMN ID ADD GENERATED ALWAYS AS IDENTITY
	(SEQUENCE NAME PUBLIC.NOTIFICATION_ID_SEQ START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1);

--
 -- TOC entry 2836 (class 0 OID 16731)
 -- Dependencies: 204
 -- Data for Name: attendee; Type: TABLE DATA; Schema: public; Owner: -
 --

INSERT INTO PUBLIC.ATTENDEE (FIRST_NAME,

																					LAST_NAME,
																					CONFERENCE_ID,
																					JOB_POSITION,
																					EMAIL,
																					COMPANY,
																					CITY,
																					STATE,
																					INTERESTS,
																					SUBMITTED_DATE,
																					COMMENTS)
VALUES ('Lanice', 'Montre', 1, 'Director', 'lamontre@gmail.com', 'Montreal Consulting Inc', 'Philadelphia', 'PA', 'ML', '2020-05-07 00:00:00-04', 'learn more'),
							('Do', 'Ji', 1, 'Director', 'mar@smith.org', 'Mafolab', 'Rockville', 'AZ', 'CC', '2020-05-07 00:00:00-04', 'networking'),
							('Edem', 'Lamoine', 1, 'Executive', 'lamoine@gmail.com', 'Paracetamole Pharma', 'Washington', 'DC', 'DS', '2020-05-07 00:00:00-04', 'Hands on experience'),
							('Celine', 'Mabs', 1, 'Developer', 'celinemabs@school.edu', 'Mabs Learning Center', 'Rawlings', 'WY', 'DS', '2020-05-07 00:00:00-04', 'Hand-ons experience and networking with engineers in the field'),
							('Mary', 'Maine', 1, 'Other', 'mary.maine@noreply.com', 'Maine Co', 'Hanover', 'PA', 'ML', '2020-05-07 00:00:00-04', 'Looking forward to start the class');

--
 -- TOC entry 2834 (class 0 OID 16722)
 -- Dependencies: 202
 -- Data for Name: conference; Type: TABLE DATA; Schema: public; Owner: -
 --

INSERT INTO PUBLIC.CONFERENCE (NAME,

																					ACTIVE, date, PRICE,

																					ADDRESS)
VALUES ('TechConf', B'1', '2022-06-10', 495, '123 Main St, Baltimore, MD 12345'),
							('TestConf', B'0', '1999-01-01', 1, '9');

--
 -- TOC entry 2838 (class 0 OID 16746)
 -- Dependencies: 206
 -- Data for Name: notification; Type: TABLE DATA; Schema: public; Owner: -
 --

INSERT INTO PUBLIC.NOTIFICATION (STATUS,

																					MESSAGE,
																					SUBMITTED_DATE,
																					COMPLETED_DATE,
																					SUBJECT)
VALUES ('Notifications submitted', ' ', NULL, NULL, ''),
							('Notifications submitted', 'uyt', '2020-05-07 18:00:38.573856-04', '2020-05-07 18:00:39.124435-04', 'Welcome Email'),
							('Notified 5 attendees', 'Welcome Email', '2020-05-07 18:14:04.239065-04', '2020-05-07 18:14:04.271981-04', 'Welcome Email'),
							('Notifications submitted', 'New Speaker Added: Dr Daniel Shu', '2020-05-07 23:24:00.504412-04', NULL, 'New Speaker Added: Dr Daniel Shu');

--
 -- TOC entry 2704 (class 2606 OID 16738)
 -- Name: attendee attendee_pkey; Type: CONSTRAINT; Schema: public; Owner: -
 --

ALTER TABLE ONLY PUBLIC.ATTENDEE ADD CONSTRAINT ATTENDEE_PKEY PRIMARY KEY (ID);

--
 -- TOC entry 2702 (class 2606 OID 16726)
 -- Name: conference conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
 --

ALTER TABLE ONLY PUBLIC.CONFERENCE ADD CONSTRAINT CONFERENCE_PKEY PRIMARY KEY (ID);

--
 -- TOC entry 2706 (class 2606 OID 16753)
 -- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
 --

ALTER TABLE ONLY PUBLIC.NOTIFICATION ADD CONSTRAINT NOTIFICATION_PKEY PRIMARY KEY (ID);

--
 -- TOC entry 2707 (class 2606 OID 16739)
 -- Name: attendee conference; Type: FK CONSTRAINT; Schema: public; Owner: -
 --

ALTER TABLE ONLY PUBLIC.ATTENDEE ADD CONSTRAINT CONFERENCE
FOREIGN KEY (CONFERENCE_ID) REFERENCES PUBLIC.CONFERENCE (ID);

-- Completed on 2020-05-08 07:52:45
 --
-- PostgreSQL database dump complete
--