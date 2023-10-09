-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Дек 23 2022 г., 19:19
-- Версия сервера: 10.5.16-MariaDB-1:10.5.16+maria~buster-log
-- Версия PHP: 7.0.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `chatbot`
--

DELIMITER $$
--
-- Процедуры
--
CREATE DEFINER=`chatbot`@`localhost` PROCEDURE `DeleteOldClients` ()  NO SQL
    COMMENT 'Удаление неоплаченных клиентов старше 90 дней'
DELETE FROM Client WHERE DateCreate < (NOW() - INTERVAL 90 DAY) AND IsPayment = 0$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `Client`
--

CREATE TABLE `Client` (
  `ID` int(11) NOT NULL COMMENT 'Уникальный ключ пациента',
  `Surname` varchar(50) NOT NULL COMMENT 'Фамилия пациента',
  `Name` varchar(50) NOT NULL COMMENT 'Имя пациента',
  `LastName` varchar(50) NOT NULL COMMENT 'Отчество пациента',
  `Telephone` varchar(12) NOT NULL COMMENT 'Телефонный номер пациента в формате +7xxxxxxxxxx цифр',
  `IsPayment` tinyint(1) NOT NULL COMMENT 'Оплачен пациент или нет. Значения от 0 до 1',
  `DateCreate` date NOT NULL COMMENT 'Дата создания клиента'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `ClientPartner`
--

CREATE TABLE `ClientPartner` (
  `ClientID` int(11) NOT NULL COMMENT 'Внешний ключ на клиента',
  `PartnerID` int(11) NOT NULL COMMENT 'Внешний ключ на партнера'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `Partner`
--

CREATE TABLE `Partner` (
  `ID` int(11) NOT NULL,
  `LoginTG` varchar(50) NOT NULL COMMENT 'Логин в телеграмме',
  `FullName` varchar(155) NOT NULL COMMENT 'ФИО',
  `Sum` int(11) NOT NULL COMMENT 'Сумма за одного клиента'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `PartnerTelegram`
--

CREATE TABLE `PartnerTelegram` (
  `ID` int(11) NOT NULL,
  `PartnerID` int(11) NOT NULL,
  `TelegramID` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `PotentialClient`
--

CREATE TABLE `PotentialClient` (
  `ID` int(11) NOT NULL,
  `Surname` varchar(50) NOT NULL COMMENT 'Фаимлия',
  `Name` varchar(50) NOT NULL COMMENT 'Имя',
  `LastName` varchar(50) NOT NULL COMMENT 'Отчество',
  `Telephone` varchar(12) NOT NULL COMMENT 'Номер телефона +7xxxxxxxxxx'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `WaitClient`
--

CREATE TABLE `WaitClient` (
  `ID` int(11) NOT NULL,
  `TelegramID` bigint(20) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `FatherName` varchar(50) DEFAULT NULL,
  `Phone` varchar(12) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `WaitData`
--

CREATE TABLE `WaitData` (
  `ID` int(11) NOT NULL,
  `AdminID` bigint(20) DEFAULT NULL,
  `ValueData` varchar(155) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `WaitForSend`
--

CREATE TABLE `WaitForSend` (
  `ID` int(11) NOT NULL,
  `PartnerID` int(11) NOT NULL,
  `ClientID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `WaitPartner`
--

CREATE TABLE `WaitPartner` (
  `ID` int(11) NOT NULL,
  `AdminID` bigint(20) DEFAULT NULL,
  `LoginTG` varchar(50) DEFAULT NULL,
  `FullName` varchar(155) DEFAULT NULL,
  `Sum` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Client`
--
ALTER TABLE `Client`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Surname` (`Surname`),
  ADD KEY `Telephone` (`Telephone`);

--
-- Индексы таблицы `ClientPartner`
--
ALTER TABLE `ClientPartner`
  ADD KEY `ClientPartner_ibfk_1` (`ClientID`),
  ADD KEY `ClientPartner_ibfk_2` (`PartnerID`);

--
-- Индексы таблицы `Partner`
--
ALTER TABLE `Partner`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `LoginTG` (`LoginTG`);

--
-- Индексы таблицы `PartnerTelegram`
--
ALTER TABLE `PartnerTelegram`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `fk_partnerID_id` (`PartnerID`);

--
-- Индексы таблицы `PotentialClient`
--
ALTER TABLE `PotentialClient`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `WaitClient`
--
ALTER TABLE `WaitClient`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `WaitData`
--
ALTER TABLE `WaitData`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `WaitForSend`
--
ALTER TABLE `WaitForSend`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `WaitPartner`
--
ALTER TABLE `WaitPartner`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Client`
--
ALTER TABLE `Client`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ключ пациента', AUTO_INCREMENT=65;
--
-- AUTO_INCREMENT для таблицы `Partner`
--
ALTER TABLE `Partner`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT для таблицы `PartnerTelegram`
--
ALTER TABLE `PartnerTelegram`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT для таблицы `PotentialClient`
--
ALTER TABLE `PotentialClient`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=207;
--
-- AUTO_INCREMENT для таблицы `WaitClient`
--
ALTER TABLE `WaitClient`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;
--
-- AUTO_INCREMENT для таблицы `WaitData`
--
ALTER TABLE `WaitData`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT для таблицы `WaitForSend`
--
ALTER TABLE `WaitForSend`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT для таблицы `WaitPartner`
--
ALTER TABLE `WaitPartner`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `ClientPartner`
--
ALTER TABLE `ClientPartner`
  ADD CONSTRAINT `ClientPartner_ibfk_1` FOREIGN KEY (`ClientID`) REFERENCES `Client` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ClientPartner_ibfk_2` FOREIGN KEY (`PartnerID`) REFERENCES `Partner` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `PartnerTelegram`
--
ALTER TABLE `PartnerTelegram`
  ADD CONSTRAINT `fk_partnerID_id` FOREIGN KEY (`PartnerID`) REFERENCES `Partner` (`ID`),
  ADD CONSTRAINT `fk_partner_id` FOREIGN KEY (`PartnerID`) REFERENCES `Partner` (`ID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
