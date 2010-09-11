#!/usr/bin/env python
import os
import cPickle

FILE_EXT = "cposs"
APP_NAME = "cposs"


class Settings:
	"""The settings class to load and save settings"""
	def __init__(self):
		self.SettingsFile='data/settings.dat'
		if os.path.isfile(self.SettingsFile):
			file = open(self.SettingsFile, "r")
			self.Settings = cPickle.load(file)
			file.close()
		else:
			print "Settings file not found, maybe you havn't defined any settings yet."
			self.Settings={}
		
	def SaveSettings(self):
		"""This is the function which saves the settings."""
		file = open(self.SettingsFile, "w")
		cPickle.dump(self.Settings, file)
		file.close()

	def GetSetting(self,SettingKey):
		"""Returns the value for the given setting key"""
		return self.Settings.get(SettingKey,'Undefined')

	def SetSetting(self,SettingKey,SettingValue):
		"""Returns the value for the given setting key"""
		self.Settings[SettingKey]=SettingValue

if __name__ == "__main__":
	Settings = Settings()
	Settings.SetSetting('Name','Philip')
	print "Setting for Name set as: %s" % Settings.GetSetting('Name')
	Settings.SaveSettings()
