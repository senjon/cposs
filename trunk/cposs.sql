-- phpMyAdmin SQL Dump
-- version 2.11.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 08, 2008 at 05:53 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.4-2ubuntu5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `cposs`
--

-- --------------------------------------------------------

--
-- Table structure for table `basket`
--

CREATE TABLE IF NOT EXISTS `basket` (
  `BasketID` mediumint(9) NOT NULL auto_increment,
  `Expiry` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `UserID` mediumint(9) NOT NULL default '1',
  `Completed` tinyint(1) NOT NULL default '0',
  PRIMARY KEY  (`BasketID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=27 ;

--
-- Dumping data for table `basket`
--

INSERT INTO `basket` (`BasketID`, `Expiry`, `UserID`, `Completed`) VALUES
(2, '2007-10-07 00:00:42', 0, 0),
(3, '2007-10-07 00:00:08', 0, 0),
(4, '2007-10-08 00:00:44', 0, 0),
(5, '2007-10-08 00:00:56', 0, 0),
(6, '2007-10-08 00:00:03', 0, 0),
(7, '2008-01-02 00:20:54', 0, 0),
(8, '2008-01-02 00:21:27', 0, 0),
(9, '2008-01-02 00:22:17', 0, 0),
(10, '2008-01-02 00:22:47', 1, 0),
(11, '2008-01-02 00:23:25', 1, 0),
(12, '2008-01-02 00:23:51', 1, 0),
(13, '2008-01-02 00:27:05', 1, 0),
(14, '2008-01-02 00:28:03', 1, 0),
(15, '2008-01-02 00:28:15', 1, 0),
(16, '2008-01-02 00:34:26', 1, 0),
(17, '2008-01-02 00:36:06', 1, 0),
(18, '2008-01-02 00:37:04', 1, 0),
(19, '2008-01-02 00:40:06', 1, 0),
(20, '2008-01-02 00:40:46', 1, 0),
(21, '2008-01-02 00:40:51', 1, 0),
(22, '2008-01-02 00:46:23', 1, 0),
(23, '2008-01-02 00:46:43', 1, 0),
(24, '2008-01-02 00:47:15', 1, 0),
(25, '2008-01-02 00:47:26', 1, 1),
(26, '2008-01-02 00:48:41', 1, 1),
(1, '2008-05-02 20:13:58', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `basket_sub`
--

CREATE TABLE IF NOT EXISTS `basket_sub` (
  `BasketItemID` mediumint(9) NOT NULL auto_increment,
  `BasketID` mediumint(9) NOT NULL default '0',
  `ItemID` mediumint(9) NOT NULL default '0',
  `Qty` smallint(6) NOT NULL default '1',
  `UnitPrice` decimal(10,2) NOT NULL default '0.00',
  PRIMARY KEY  (`BasketItemID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=54 ;

--
-- Dumping data for table `basket_sub`
--

INSERT INTO `basket_sub` (`BasketItemID`, `BasketID`, `ItemID`, `Qty`, `UnitPrice`) VALUES
(3, 2, 4, 21, '0.00'),
(4, 2, 3, 7, '0.00'),
(5, 2, 1, -2, '0.00'),
(6, 1, 4, 4, '0.00'),
(7, 3, 3, 1, '0.00'),
(8, 3, 4, 1, '0.00'),
(9, 4, 4, 1, '0.00'),
(10, 4, 3, 1, '0.00'),
(11, 5, 4, 5, '0.00'),
(12, 5, 3, 5, '0.00'),
(13, 6, 4, 1, '0.00'),
(39, 2, 2, 15, '0.00'),
(40, 15, 2, 1, '0.00'),
(41, 16, 2, 0, '0.00'),
(42, 17, 2, 0, '0.00'),
(43, 18, 2, 0, '0.00'),
(44, 19, 2, 0, '0.00'),
(45, 22, 2, 0, '0.00'),
(46, 23, 2, 0, '0.00'),
(47, 24, 2, 0, '0.00'),
(48, 25, 2, 0, '0.00'),
(49, 26, 2, 0, '0.00'),
(51, 2, 5, 1, '0.00'),
(52, 3, 2, 1, '0.00'),
(53, 3, 5, 1, '0.00');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
  `CategoryID` smallint(6) NOT NULL auto_increment,
  `Category` text NOT NULL,
  `Description` text NOT NULL,
  `Added` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `Updated` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`CategoryID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`CategoryID`, `Category`, `Description`, `Added`, `Updated`) VALUES
(1, 'General', 'This is the department for everything', '0000-00-00 00:00:00', '2007-10-06 18:25:37'),
(2, 'Jumpers', 'We have a lovely collection of Jumpers\n', '0000-00-00 00:00:00', '2007-10-06 18:24:01'),
(3, 'Skirts', 'This department is full of skirts', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(4, 'Coats', 'Coats is the department here', '0000-00-00 00:00:00', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE IF NOT EXISTS `departments` (
  `DepartmentID` smallint(6) NOT NULL auto_increment,
  `Department` text NOT NULL,
  `Description` text NOT NULL,
  `Added` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `Updated` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`DepartmentID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`DepartmentID`, `Department`, `Description`, `Added`, `Updated`) VALUES
(1, 'General', 'This is the department for everything', '0000-00-00 00:00:00', '2007-10-06 18:25:37'),
(2, 'Jumpers', 'We have a lovely collection of Jumpers\n', '0000-00-00 00:00:00', '2007-10-06 18:24:01'),
(3, 'Skirts', 'This department is full of skirts', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(4, 'Coats', 'Coats is the department here', '0000-00-00 00:00:00', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `discounts`
--

CREATE TABLE IF NOT EXISTS `discounts` (
  `DiscountID` smallint(6) NOT NULL auto_increment,
  `DiscountName` text NOT NULL,
  `DiscountType` smallint(6) NOT NULL COMMENT 'EXPLAIN HERE THE TYPES, ALSO EXPLAIN IN LOGIC',
  `DiscountValue` mediumint(9) NOT NULL,
  PRIMARY KEY  (`DiscountID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `discounts`
--

INSERT INTO `discounts` (`DiscountID`, `DiscountName`, `DiscountType`, `DiscountValue`) VALUES
(1, 'Half price sale', 1, 50),
(2, 'Multibuy', 2, 20),
(3, 'Percentage discount', 3, 25);

-- --------------------------------------------------------

--
-- Table structure for table `discounts_sub`
--

CREATE TABLE IF NOT EXISTS `discounts_sub` (
  `DiscountID` smallint(6) NOT NULL,
  `ItemID` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `discounts_sub`
--

INSERT INTO `discounts_sub` (`DiscountID`, `ItemID`) VALUES
(1, 3),
(2, 2),
(2, 5),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE IF NOT EXISTS `products` (
  `ProductID` mediumint(9) NOT NULL auto_increment,
  `Added` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `Updated` timestamp NOT NULL default '0000-00-00 00:00:00',
  `Heading` text NOT NULL,
  `Description` text NOT NULL,
  `Price` bigint(20) NOT NULL,
  `ImageName` text NOT NULL,
  PRIMARY KEY  (`ProductID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`ProductID`, `Added`, `Updated`, `Heading`, `Description`, `Price`, `ImageName`) VALUES
(1, '2007-10-10 16:51:07', '2007-10-10 16:51:07', 'Payment Method', 'This is a payment method product. It enables barcode scanning of payments', 0, ''),
(2, '2008-05-02 19:54:12', '2007-10-08 13:00:08', 'Horrible Coat', 'Horrible coat, you really wouldn''t like to buy....\nOr would you?\n\n\n\n\n\n\n\n\n\n\n', 500, '2.jpg'),
(3, '2007-10-08 12:49:55', '2007-10-08 12:49:55', 'None', '\n', 0, '3.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `productscategories`
--

CREATE TABLE IF NOT EXISTS `productscategories` (
  `ProductID` mediumint(9) NOT NULL default '1',
  `CategoryID` mediumint(9) NOT NULL,
  PRIMARY KEY  (`ProductID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='This is the table that specifies all the products in departs';

--
-- Dumping data for table `productscategories`
--


-- --------------------------------------------------------

--
-- Table structure for table `productsdepartments`
--

CREATE TABLE IF NOT EXISTS `productsdepartments` (
  `ProductID` mediumint(9) NOT NULL default '1',
  `DepartmentID` mediumint(9) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='This is the table that specifies all the products in departs';

--
-- Dumping data for table `productsdepartments`
--


-- --------------------------------------------------------

--
-- Table structure for table `products_sub`
--

CREATE TABLE IF NOT EXISTS `products_sub` (
  `ItemID` bigint(20) NOT NULL auto_increment,
  `ProductID` mediumint(9) NOT NULL,
  `Detail1` text NOT NULL,
  `Detail2` text,
  PRIMARY KEY  (`ItemID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `products_sub`
--

INSERT INTO `products_sub` (`ItemID`, `ProductID`, `Detail1`, `Detail2`) VALUES
(1, 1, 'Cash', NULL),
(2, 1, 'Credit Card', NULL),
(3, 2, 'Pink', 'Small'),
(4, 2, 'Black', 'Large'),
(5, 2, 'Horrendous', 'Need to get rid of this bad boy');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `UserID` mediumint(9) NOT NULL auto_increment,
  `Email` text NOT NULL,
  `Password` text NOT NULL,
  `Name` text NOT NULL,
  PRIMARY KEY  (`UserID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `users`
--

