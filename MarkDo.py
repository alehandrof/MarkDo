#!/usr/bin/python

import re
import sublime
import sublime_plugin
import datetime

class MarkdoAddCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			current_scope = self.view.scope_name(self.view.sel()[0].b)
			if not current_scope == 'text.html.markdown.do ': # insufficient!
				self.view.run_command('run_macro_file', { 'file': 'Packages/Default/Add Line.sublime-macro' } )
			# self.view.run_command('insert_snippet', { 'contents': '%s ${1:What\'s the next action?} %s(%s)' % (self.open_tasks_bullet, self.added_tag, datetime.now().strftime(self.date_format)) } )
			self.view.run_command('insert_snippet', { 'contents': '- [ ] ${1:}  +%s' % (datetime.date.today().isoformat()) })
			# self.view.run_command('indent')

class MarkdoCheckboxCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			line = self.view.line(region)
			contents = self.view.substr(line).rstrip()
			scope = self.view.extract_scope(region.end())
			checkbox = self.view.substr(scope)
			# print '>' + checkbox+'<'
			if '[ ] ' in checkbox:
				# print 'Check'
				# checkbox = checkbox.replace('[ ]', '[x]')
				# self.view.replace(edit, scope, checkbox)
				self.view.run_command('markdo_complete')
			# if 'incomplete' in current_scope:
			# if re.match('^(\\s*[-\\+\\*]\\s\\[ \\])', contents)
			# self.view.replace(edit, line, '+')
			# self.view.insert(edit, line.end(), ' #done:' + datetime.date.today().isoformat())

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
			if re.match('.*(([-\+\*] )?\[xX\])', contents): # Complete
				new_contents = re.sub(r'(\[xX\])(.*) x.*', r'[ ]\2', contents)
				# print new_contents
			if re.match('.*(([-\+\*] )?\[ \])', contents): # Incomplete
				new_contents = re.sub(r'(\[ \])(.*)', r'[x]\2 x' + datetime.date.today().isoformat(), contents)
				# print new_contents
			self.view.replace(edit, line, new_contents)