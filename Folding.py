# http://www.sublimetext.com/forum/viewtopic.php?f=4&t=7963&sid=868b19cbbc0445e34140fd49b13a5ca9

import sublime, sublime_plugin

class AllCommand(sublime_plugin.TextCommand):

	# def done(self,foldstr):
		# self.foldstr = arg
		# self.all(foldstr)

	def all(self, foldstr):
		view = self.view
		# print "All {" + foldstr + "}"
		view.run_command("unfold_all")
		endline, endcol = view.rowcol(view.size())
		line = 0
		firstRegion = None
		currRegion = None
		regions = []

		while line < endline:
			region = view.full_line(view.text_point(line, 0))
			data = view.substr(region)
			if data.find(foldstr) == -1:
				if firstRegion == None:
					firstRegion = region
					lastRegion  = region
				else:
					lastRegion  = region
			else:
				if firstRegion:
					# currRegion = firstRegion.cover(lastRegion)
					currRegion = \
						sublime.Region(sublime.Region.begin(firstRegion) - 1, \
						sublime.Region.end(lastRegion) - 1 )
					regions.append(currRegion)
					firstRegion = None
			line += 1
			if currRegion:
				regions.append(currRegion)
				currRegion = None

		if firstRegion:
			currRegion = firstRegion.cover(lastRegion)
			regions.append(currRegion)
			firstRegion = None
		view.fold(regions)
		# view.settings().set("all", foldstr)
		view.run_command("show_at_center")

	def run(self, edit, foldstr=""):
		### The following forbids the command from running twice
		# if self.view.settings().has("all"):
		# 	self.done(self.view.settings().get("all"))
		# 	return
		window = self.view.window()
		# print foldstr
		if not foldstr:
			for reg in self.view.sel():
				foldstr = self.view.substr(reg)
				self.all(foldstr)
				break
		if not foldstr:
			window.show_input_panel("Show Only Lines Containing", foldstr, self.all, None, None)
		else:
			self.all(foldstr)


class AllToggleCommand(sublime_plugin.TextCommand):
	def run(self, edit, foldstr):
		view = self.view
		# if view.settings().has("all"):
		if len(view.folded_regions()):
			view.run_command("unfold_all")
			# foldstr = ""
			# view.settings().set("all", foldstr)
			view.run_command("show_at_center")
		else:
			view.run_command("all", { "foldstr": foldstr })
