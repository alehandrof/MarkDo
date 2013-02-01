#!/usr/bin/python

import re
import sublime
import sublime_plugin
import datetime

markdo_timestamp = datetime.date.today().isoformat()

class MarkdoAddCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			current_scope = self.view.scope_name(self.view.sel()[0].b)
			if not current_scope == 'text.html.markdown.do ': # insufficient!
				self.view.run_command('run_macro_file', { 'file': 'Packages/Default/Add Line.sublime-macro' } )
			# self.view.run_command('insert_snippet', { 'contents': '%s ${1:What\'s the next action?} %s(%s)' % (self.open_tasks_bullet, self.added_tag, datetime.now().strftime(self.date_format)) } )
			self.view.run_command('insert_snippet', { 'contents': '- [ ] ${1:}  +%s' % markdo_timestamp })
			# self.view.run_command('indent')

class MarkdoCheckboxCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			line = self.view.line(region)
			contents = self.view.substr(line).rstrip()
			scope = self.view.extract_scope(region.end())
			checkbox = self.view.substr(scope)
			print '>' + checkbox+'<'
			# if '[ ] ' in checkbox:
			if re.match('(\[[ xX]\]\s)', checkbox):
				# print 'Check'
				# checkbox = checkbox.replace('[ ]', '[x]')
				# self.view.replace(edit, scope, checkbox)
				self.view.run_command('markdo_complete')
			# if 'incomplete' in current_scope:
			# if re.match('^(\\s*[-\\+\\*]\\s\\[ \\])', contents)
			# self.view.replace(edit, line, '+')
			# self.view.insert(edit, line.end(), ' #done:' + markdo_timestamp)

class MarkdoCompleteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			line = self.view.line(region)
			contents = self.view.substr(line).rstrip()
			# current_scope = self.view.scope_name(self.view.sel()[0].b)
			# if 'incomplete' in current_scope:
			# if re.match('^(\\s*[-\\+\\*]\\s\\[ \\])', contents)
			# Incomplete
			# print contents
			if re.match('.*(([-\+\*]\s)?\[[xX]\])', contents): # Action is Complete
				new_contents = re.sub(r'(\[[xX]\])(.*) x.*', r'[ ]\2', contents)
				# print new_contents
			if re.match('.*(([-\+\*]\s)?\[ \])', contents): # Action is Incomplete
				new_contents = re.sub(r'(\[ \])(.*)', r'[x]\2 x' + markdo_timestamp, contents)
				# print new_contents
			self.view.replace(edit, line, new_contents)

class MarkdoTouchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			line = self.view.line(region)
			contents = self.view.substr(line).rstrip()
			touch = ' .' + markdo_timestamp
			if re.match('.*(([-\+\*]\s)?\[ \])', contents): # Action is Incomplete
				if not re.match('\s\.'+markdo_timestamp, contents): # Action is touched already with the same string
					# new_contents = re.sub(r'(\[ \])(.*)', r'[x]\2 x' + markdo_timestamp, contents)
					self.view.insert(edit, line.end(), touch)
					# self.view.replace(edit, line, new_contents)