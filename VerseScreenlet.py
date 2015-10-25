#!/usr/bin/env python

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#  VerseScreenlet (c) RYX 2007 <ryx@ryxperience.com>
#
# INFO:
# - a simple screenlet to show verse

import screenlets
from screenlets.options import *
from screenlets.options import create_option_from_node
from screenlets import DefaultMenuItem
import pango
import gobject
import gtk
import random
import inspect, os


class VerseScreenlet (screenlets.Screenlet):
	"""A simple example of how to create a Screenlet"""
	
	# default meta-info for Screenlets (should be removed and put into metainfo)
	__name__	= 'VerseScreenlet'
	__version__	= '0.1'
	__author__	= 'Timophey'
	__desc__	= __doc__	# set description to docstring of class
	
	option_width = 450
	option_height = 180
	option_height_calc = 0
	option_padding = 10
	
	# editable options (options that are editable through the UI)
	timer = 1
	color_verse = (255, 255, 255, 1)
	color_verse_back = (0.0, 0.0, 0.0, 1)
	background_color = (255, 255, 255, 0)
	background_image = ''
	font_verse = "Georgia italic 20"
	back_offset_x = -1
	back_offset_y = -1
	hover = False
	number = 0
	list_file = ''
	items = []
	item_index = 0
	# constructor
	def __init__ (self, **keyword_args):
		#call super (width/height MUST match the size of graphics in the theme)
		screenlets.Screenlet.__init__(self, width=self.option_width, height=self.option_height, 
			uses_theme=False, **keyword_args)
		# set theme
		# self.theme_name = "png"
		# add option group
		self.add_options_group('Verse', 'This is options of  verses screenlet')
		# setup
		self.add_option(IntOption('Verse','option_width', self.option_width, 'Width', '', min=50, max=2000))
		self.add_option(IntOption('Verse','option_height', self.option_height, 'Height', '', min=50, max=2000))
		self.add_option(IntOption('Verse','option_padding', self.option_padding, 'Padding', '', min=0, max=50))
		self.add_option(ColorOption('Verse','background_color', self.background_color, 'Background color', 'Color of text'))
		self.add_option(ImageOption('Verse','background_image', self.background_image, 'Background image', 'Example options group using Image')) 		
		
		self.add_option(IntOption('Verse','timer', self.timer, 'Timer', 'Timer to change verse', min=0, max=7200))
		
		self.add_option(FontOption('Verse','font_verse', self.font_verse, 'Font', 'Font to display text'))
		self.add_option(ColorOption('Verse','color_verse', self.color_verse, 'Text color', 'Color of text'))
		self.add_option(ColorOption('Verse','color_verse_back', self.color_verse_back, 'Text color behind', 'Color of text behind'))
		
		self.add_option(IntOption('Verse','back_offset_x', self.back_offset_x, 'Back offset x', '', min=-10, max=10))
		self.add_option(IntOption('Verse','offset_y', self.back_offset_y, 'Back offset y', '', min=-10, max=10))

		self.add_option(FileOption('Verse','list_file', self.list_file, 'List file', 'File contains list ov verses')) 

		# ADD a 1 second (1000) TIMER
		self.timer = gobject.timeout_add( 1000, self.update)
		#Also add options from xml file for example porpuse
		self.init_options_from_metadata()

	def update (self):
		if self.number < self.timer:
			self.number = self.number+1
		else:
			self.number = 0
			self.item_index = random.randint(0,len(self.items)-1)
		if self.option_height_calc > 0 and self.option_height_calc != self.option_height:
			self.option_height = self.option_height_calc
		self.redraw_canvas()
		return True # keep running this event	
	
	# ONLY FOR TESTING!!!!!!!!!
	def init_options_from_metadata (self):
		"""Try to load metadata-file with options. The file has to be named
		like the Screenlet, with the extension ".xml" and needs to be placed
		in the Screenlet's personal directory. 
		NOTE: This function always uses the metadata-file relative to the 
			  Screenlet's location, not the ones in SCREENLETS_PATH!!!"""
		p = __file__.rfind('/')
		mypath = __file__[:p]
		#self.add_options_from_file( mypath + '/' + self.__class__.__name__ + '.xml')	


	def on_after_set_atribute(self,name, value):
		"""Called after setting screenlet atributes"""
		#print name + ' is going to change from ' + str(value)
		if name == 'list_file':
			self.conflig_load()
		pass

	def on_before_set_atribute(self,name, value):
		"""Called before setting screenlet atributes"""
		#print name + ' has changed to ' + str(value)
		if name in('option_width','option_height'):
			self.width = self.option_width
			self.height = self.option_height
		pass


	def on_create_drag_icon (self):
		"""Called when the screenlet's drag-icon is created. You can supply
		your own icon and mask by returning them as a 2-tuple."""
		return (None, None)

	def on_composite_changed(self):
		"""Called when composite state has changed"""
		pass

	def on_drag_begin (self, drag_context):
		"""Called when the Screenlet gets dragged."""
		pass
	
	def on_drag_enter (self, drag_context, x, y, timestamp):
		"""Called when something gets dragged into the Screenlets area."""
		pass
	
	def on_drag_leave (self, drag_context, timestamp):
		"""Called when something gets dragged out of the Screenlets area."""
		pass

	def on_drop (self, x, y, sel_data, timestamp):
		"""Called when a selection is dropped on this Screenlet."""
		return False
		
	def on_focus (self, event):
		"""Called when the Screenlet's window receives focus."""
		pass
	
	def on_hide (self):
		"""Called when the Screenlet gets hidden."""
		pass
	
	def on_init (self):
		"""Called when the Screenlet's options have been applied and the 
		screenlet finished its initialization. If you want to have your
		Screenlet do things on startup you should use this handler."""
		if self.list_file == '':
			path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
			self.list_file = path+"/lists/russian.txt"
		# add default menu items
		self.add_default_menuitems()
		# load resources
		self.conflig_load()


#	def on_key_down(self, keycode, keyvalue, event):
#		"""Called when a keypress-event occured in Screenlet's window."""
#		key = gtk.gdk.keyval_name(event.keyval)
#		
#		if key == "Return" or key == "Tab":
#			screenlets.show_message(self, 'This is the ' + self.__name__ +'\n' + 'It is installed in ' + self.__path__)
#	
	def on_load_theme (self):
		"""Called when the theme is reloaded (after loading, before redraw)."""
		pass
	
	def on_menuitem_select (self, id):
		"""Called when a menuitem is selected."""
		if id == "at_runtime":
			screenlets.show_message(self, 'This is an example on a menu created at runtime')
		if id == "at_xml":
			screenlets.show_message(self, 'This is an example on a menu created in the menu.xml')
		pass
	
	def on_mouse_down (self, event):
		"""Called when a buttonpress-event occured in Screenlet's window. 
		Returning True causes the event to be not further propagated."""
		return False
	
	def on_mouse_enter (self, event):
		"""Called when the mouse enters the Screenlet's window."""
		#self.show_tooltip("this is a tooltip , it is set to shows on mouse hover",self.x+self.mousex,self.y+self.mousey)
		self.hover = True
		#print 'mouse is over me'
		
	def on_mouse_leave (self, event):
		"""Called when the mouse leaves the Screenlet's window."""
		self.hide_tooltip()
		self.hover = False
		#print 'mouse leave'

	def on_mouse_move(self, event):
		"""Called when the mouse moves in the Screenlet's window."""
		self.redraw_canvas()
		pass

	def on_mouse_up (self, event):
		"""Called when a buttonrelease-event occured in Screenlet's window. 
		Returning True causes the event to be not further propagated."""
		self.number = self.timer
		self.update()
		return False
	
	def on_quit (self):
		"""Callback for handling destroy-event. Perform your cleanup here!"""
		#screenlets.show_question(self, 'Do you like screenlets?')
		return True
		
	def on_realize (self):
		""""Callback for handling the realize-event."""
	
	def on_scale (self):
		"""Called when Screenlet.scale is changed."""
		pass
	
	def on_scroll_up (self):
		"""Called when mousewheel is scrolled up (button4)."""
		pass

	def on_scroll_down (self):
		"""Called when mousewheel is scrolled down (button5)."""
		pass
	
	def on_show (self):
		"""Called when the Screenlet gets shown after being hidden."""
		pass
	
	def on_switch_widget_state (self, state):
		"""Called when the Screenlet enters/leaves "Widget"-state."""
		pass
	
	def on_unfocus (self, event):
		"""Called when the Screenlet's window loses focus."""
		pass
	
	def on_draw (self, ctx):
		# if theme is loaded
		# if self.theme:
			# set scale rel. to scale-attribute
			ctx.scale(self.scale, self.scale)
			items = self.items
			# background
			ctx.set_source_rgba(self.background_color[0], self.background_color[1], self.background_color[2],self.background_color[3])
			self.draw_rounded_rectangle(ctx, 0, 0, 20, self.width, self.height)
			# verses
			if len(self.items) > 0:
				#print self.item_index
				print self.font_verse
				# split font option
				font_a = self.font_verse.split(' ')
				font_s = font_a[font_a.__len__()-1]
				# print message
				text = self.items[self.item_index]
				text_a = text.split("\t")
				text_verse = text_a[0]
				text_addr = text_a[1]
				print text_verse
				print text_addr
				# draw verse
				ctx.set_source_rgba(self.color_verse_back[0], self.color_verse_back[1], self.color_verse_back[2],self.color_verse_back[3])
				self.draw_text(ctx, text, self.option_padding + self.back_offset_x, self.option_padding + self.back_offset_y, self.font_verse , font_s, self.width - self.option_padding * 2)
				ctx.set_source_rgba(self.color_verse[0], self.color_verse[1], self.color_verse[2],self.color_verse[3])
				self.draw_text(ctx, text, self.option_padding, self.option_padding, self.font_verse , font_s, self.width - self.option_padding * 2)
				# calc position
				#vertical_offset = self.get_text_height(ctx, text_verse, self.font_verse)
				#text_addr_width = self.get_text_width(ctx, text_addr, self.font_verse)
				#text_addr_height = self.get_text_height(ctx, text_addr, self.font_verse)
				# draw address
				#ctx.set_source_rgba(self.color_verse_back[0], self.color_verse_back[1], self.color_verse_back[2],self.color_verse_back[3])
				#self.draw_text(ctx, text_addr, self.option_padding + self.back_offset_x, self.option_padding + vertical_offset + text_addr_height * 0.25 + self.back_offset_y, self.font_verse , font_s, self.width - self.option_padding * 2, pango.ALIGN_RIGHT)
				#ctx.set_source_rgba(self.color_verse[0], self.color_verse[1], self.color_verse[2],self.color_verse[3])
				#self.draw_text(ctx, text_addr, self.option_padding, self.option_padding + vertical_offset + text_addr_height * 0.25, self.font_verse , font_s, self.width - self.option_padding * 2, pango.ALIGN_RIGHT)
				#self.option_height_calc = vertical_offset + text_addr_height + self.option_padding * 2

	def conflig_load(self):
		myfile = open(self.list_file, "rU")
		data = []
		verses = []
		for line in myfile.xreadlines():
			if len(line) > 4:
				sw = line[0:1]
				if sw == '#' or sw == ";":
					data.append(line)
				else:
					verses.append(line)
		#out = {'config':data,'verses':verses}
		self.items = verses
		self.item_index = random.randint(0,len(self.items)-1)
		return 0
	
	def on_draw_shape (self, ctx):
		self.on_draw(ctx)
	
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	# create new session
	import screenlets.session
	screenlets.session.create_session(VerseScreenlet)
