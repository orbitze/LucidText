#!/usr/bin/python3

import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GObject


class SearchDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Search and Mark", transient_for=parent, modal=True)
        self.add_buttons(
            Gtk.STOCK_FIND,
            Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL
        )

        self.set_border_width(10)
        box = self.get_content_area()

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.show_all()


class FindReplaceDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Find and Replace", transient_for=parent, modal=True)
        self.add_buttons(
            Gtk.STOCK_FIND_AND_REPLACE,
            Gtk.ResponseType.APPLY,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL
        )

        self.set_border_width(10)
        box = self.get_content_area()

        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, spacing=5)

        self.find_label = Gtk.Label(label="Find:")
        self.replace_label = Gtk.Label(label="Replace:")
        self.find_entry = Gtk.Entry()
        self.replace_entry = Gtk.Entry()

        vbox.add(self.find_label)
        vbox.add(self.find_entry)
        vbox.add(self.replace_label)
        vbox.add(self.replace_entry)

        box.add(vbox)

        self.show_all()


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_border_width(10)
        self.set_size_request(900, 700)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.create_textview() 
        self.create_toolbar()
        self.create_buttons()

        self.show_all()


    def create_toolbar(self):
        icon_theme = Gtk.IconTheme.get_default()

        self.hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, spacing=2)
        self.grid.attach(self.hbox, 0, 0, 3, 1)

        toolbar1 = Gtk.Toolbar.new()
        toolbar1.set_show_arrow(True)
        toolbar1.set_style(Gtk.ToolbarStyle.ICONS)

        # Open
        icon = icon_theme.load_icon("document-open-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        openb = Gtk.ToolButton.new(image)
        openb.connect("clicked", self.on_open_clicked)
        toolbar1.insert(openb, 0)

        # New
        icon = icon_theme.load_icon("document-new-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        new = Gtk.ToolButton.new(image)
        new.connect("clicked", self.on_new_clicked)
        toolbar1.insert(new, 1)

        # Save 
        icon = icon_theme.load_icon("document-save-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        save = Gtk.ToolButton.new(image)
        save.connect("clicked", self.on_save_clicked)
        toolbar1.insert(save, 2)

        toolbar1.insert(Gtk.SeparatorToolItem(), 4)

        # Cut
        icon = icon_theme.load_icon("edit-cut-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        cut = Gtk.ToolButton.new(image)
        cut.connect("clicked", self.on_cut_clicked)
        toolbar1.insert(cut, 5)

        # Copy
        icon = icon_theme.load_icon("edit-copy-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        copy = Gtk.ToolButton.new(image)
        copy.connect("clicked", self.on_copy_clicked)
        toolbar1.insert(copy, 6)

        # Paste
        icon = icon_theme.load_icon("edit-paste-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        paste = Gtk.ToolButton.new(image)
        paste.connect("clicked", self.on_paste_clicked)
        toolbar1.insert(paste, 7)

        toolbar1.insert(Gtk.SeparatorToolItem(), 8)

        # Clear All
        icon = icon_theme.load_icon("edit-clear-all-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        clearall = Gtk.ToolButton.new(image)
        clearall.connect("clicked", self.on_clearall_clicked)
        toolbar1.insert(clearall, 9)

        toolbar1.insert(Gtk.SeparatorToolItem(), 10)
        
        # Undo
        icon = icon_theme.load_icon("edit-undo-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        undo = Gtk.ToolButton.new(image)
        # undo.connect("clicked", self.on_paste_clicked)
        toolbar1.insert(undo, 11)

        # Redo
        icon = icon_theme.load_icon("edit-redo-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        redo = Gtk.ToolButton.new(image)
        # redo.connect("clicked", self.on_paste_clicked)
        toolbar1.insert(redo, 12)

        toolbar1.insert(Gtk.SeparatorToolItem(), 13)

        # Search and Mark
        icon = icon_theme.load_icon("system-search-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        search = Gtk.ToolButton.new(image)
        search.connect("clicked", self.on_search_clicked)
        toolbar1.insert(search, 14)

        # Find and Replace
        icon = icon_theme.load_icon("edit-find-replace-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        find = Gtk.ToolButton.new(image)
        find.connect("clicked", self.on_find_clicked)
        toolbar1.insert(find, 15)

        toolbar1.insert(Gtk.SeparatorToolItem(), 16)

        self.hbox.pack_start(toolbar1, False, False, 0)

        ## SET FONT BUTTON  ####
        font = Gtk.FontButton.new()
        font.connect("font_set", self.on_font_changed)

        self.hbox.pack_start(font, False, False, 0)

        toolbar2 = Gtk.Toolbar.new()
        toolbar2.set_show_arrow(True)
        toolbar2.set_style(Gtk.ToolbarStyle.ICONS)

        toolbar2.insert(Gtk.SeparatorToolItem(), 0)

        # Justify Left
        radio_justifyleft = Gtk.RadioToolButton()
        radio_justifyleft.set_icon_name("format-justify-left-symbolic")
        radio_justifyleft.connect("toggled", self.on_justify_toggled, Gtk.Justification.LEFT)
        toolbar2.insert(radio_justifyleft, 1)

        # Justify Center
        radio_justifycenter = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifycenter.set_icon_name("format-justify-center-symbolic")
        radio_justifycenter.connect("toggled", self.on_justify_toggled, Gtk.Justification.CENTER)
        toolbar2.insert(radio_justifycenter, 2)

        # Justify Right
        radio_justifyright = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifyright.set_icon_name("format-justify-right-symbolic")
        radio_justifyright.connect("toggled", self.on_justify_toggled, Gtk.Justification.RIGHT)
        toolbar2.insert(radio_justifyright, 3)

        # Justify Fill
        radio_justifyfill = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifyfill.set_icon_name("format-justify-fill-symbolic")
        radio_justifyfill.connect("toggled", self.on_justify_toggled, Gtk.Justification.FILL)
        toolbar2.insert(radio_justifyfill, 4)

        toolbar2.insert(Gtk.SeparatorToolItem(), 5)

        # Bold
        icon = icon_theme.load_icon("format-text-bold-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        bold = Gtk.ToolButton.new(image)
        bold.connect("clicked", self.on_format_clicked, self.tag_bold)
        toolbar2.insert(bold, 6)

        # Italic
        icon = icon_theme.load_icon("format-text-italic-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        italic = Gtk.ToolButton.new(image)
        italic.connect("clicked", self.on_format_clicked, self.tag_italic)
        toolbar2.insert(italic, 7)

        # Underline
        icon = icon_theme.load_icon("format-text-underline-symbolic", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        underline = Gtk.ToolButton.new(image)
        underline.connect("clicked", self.on_format_clicked, self.tag_underline)
        toolbar2.insert(underline, 8)

        toolbar2.insert(Gtk.SeparatorToolItem(), 9)

        # Clear
        icon = icon_theme.load_icon("edit-clear", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        clear = Gtk.ToolButton.new(image)
        clear.connect("clicked", self.on_clear_clicked)
        toolbar2.insert(clear, 10)     

        toolbar2.insert(Gtk.SeparatorToolItem(), 11)

        # Quit
        icon = icon_theme.load_icon("window-close", -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        quit = Gtk.ToolButton.new(image)
        quit.connect("clicked", self.on_quit_clicked)
        # toolbar2.insert(quit, 12)

        self.hbox.pack_start(toolbar2, False, False, 0)


    def create_textview(self):
        scrolled_win = Gtk.ScrolledWindow()
        scrolled_win.set_hexpand(True)
        scrolled_win.set_vexpand(True)
        scrolled_win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.grid.attach(scrolled_win, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textview.set_top_margin(20)
        self.textview.set_left_margin(10)
        self.textview.set_right_margin(10)
        self.textview.set_bottom_margin(20)       
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)    
        scrolled_win.add(self.textview)

        self.textbuffer = self.textview.get_buffer()
        self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag("underline", underline=Pango.Underline.SINGLE)
        self.tag_found = self.textbuffer.create_tag("found", background="yellow")


    def create_buttons(self):
        self.hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
        self.grid.attach(self.hbox, 0, 2, 3, 1)

        check_editable = Gtk.CheckButton(label="Editable")
        check_editable.set_active(True)
        check_editable.connect("toggled", self.on_editable_toggled)
        self.hbox.pack_start(check_editable, True, True, 0)

        check_cursor = Gtk.CheckButton(label="Cursor Visible")
        check_cursor.set_active(True)
        check_cursor.connect("toggled", self.on_cursor_toggled)
        self.hbox.pack_start(check_cursor, True, True, 0)

        radio_wrapword = Gtk.RadioButton.new_with_label_from_widget(None, "Word Wrapping")
        radio_wrapword.connect("toggled", self.on_wrap_toggled, Gtk.WrapMode.WORD)
        self.hbox.pack_start(radio_wrapword, True, True, 0)

        radio_wrapchar = Gtk.RadioButton.new_with_label_from_widget(radio_wrapword, "Char Wrapping")
        radio_wrapchar.connect("toggled", self.on_wrap_toggled, Gtk.WrapMode.CHAR)
        self.hbox.pack_start(radio_wrapchar, True, True, 0)
        
        radio_wrapnone = Gtk.RadioButton.new_with_label_from_widget(radio_wrapword, "No Wrapping")
        radio_wrapnone.connect("toggled", self.on_wrap_toggled, Gtk.WrapMode.NONE)
        self.hbox.pack_start(radio_wrapnone, True, True, 0)

        radio_wrapcharword = Gtk.RadioButton.new_with_label_from_widget(radio_wrapword, "Word-Char Wrapping")
        radio_wrapcharword.connect("toggled", self.on_wrap_toggled, Gtk.WrapMode.WORD_CHAR)
        # self.hbox.pack_start(radio_wrapcharword, True, True, 0)


    def on_new_clicked(self, button): 
       dialog = Gtk.MessageDialog(title="Create New File", parent=self, modal=True)
       dialog.set_border_width(10)
       dialog.add_button("Yes", Gtk.ResponseType.YES)
       dialog.add_button("No", Gtk.ResponseType.NO)
       dialog.props.text = "All changes will be lost.\nDo you want to continue?"
       dialog.show_all()
       response = dialog.run()
       if response == Gtk.ResponseType.YES:
           self.textbuffer.set_text("")
       dialog.destroy()


    def on_open_clicked(self, button): 
        dialog = Gtk.FileChooserDialog(
            title="Choose a File", 
            parent=self,
            flags=Gtk.FileChooserAction.OPEN,
            buttons=(
                "Open", Gtk.ResponseType.APPLY, 
                "Cancel", Gtk.ResponseType.CANCEL
            )
        )
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.APPLY:
            file = dialog.get_filename()
            f = open(file, mode='r', encoding='utf-8')
            content = f.read()
            f.close()
            self.textbuffer.set_text(content)
        dialog.destroy()


    def on_save_clicked(self, button): 
        dialog = Gtk.FileChooserDialog(
            title="Save the File", 
            parent=self,
            flags=Gtk.FileChooserAction.SAVE,
            buttons=(
                "Save", Gtk.ResponseType.APPLY, 
                "Cancel", Gtk.ResponseType.CANCEL
            )
        )
        Gtk.FileChooser.set_extra_widget(dialog, Gtk.Entry())
        response = dialog.run()
        if response == Gtk.ResponseType.APPLY:
            file = dialog.get_filename()
            (start, end) = self.textbuffer.get_bounds()
            content = self.textbuffer.get_text(start, end, True)
            f = open(file, 'w')
            f.write(content)
            f.close()
        dialog.destroy()


    def on_font_changed(self, button):
        font = button.get_font()
        desc = Pango.font_description_from_string(font)
        self.textview.override_font(desc)


    def on_cut_clicked(self, button): 
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.textbuffer.cut_clipboard(clipboard, True)


    def on_copy_clicked(self, button): 
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.textbuffer.copy_clipboard(clipboard)


    def on_paste_clicked(self, button): 
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.textbuffer.paste_clipboard(clipboard, None, True)
        

    def on_clearall_clicked(self, button):
        self.textbuffer.set_text("")


    def on_format_clicked(self, button, tag):
        bounds = self.textbuffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.textbuffer.apply_tag(tag, start, end)


    def on_justify_toggled(self, widget, justification):
        self.textview.set_justification(justification)


    def on_clear_clicked(self, button):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.remove_all_tags(start, end)


    def on_search_clicked(self, widget):
        dialog = SearchDialog(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            cursor_mark = self.textbuffer.get_insert()
            start = self.textbuffer.get_iter_at_mark(cursor_mark)
            
            if start.get_offset() == self.textbuffer.get_char_count():
                start = self.textbuffer.get_start_iter()

            self.count = 0
            search_str = dialog.entry.get_text()
            self.search_and_mark(search_str, start)

            if self.count == 0:
                output = "\"" + search_str + "\" was not found!"
            else:
                output = str(self.count) + " occurrences of \"" + search_str + "\" found!"
            
            search_result_dialog = Gtk.MessageDialog(
                parent=self,
                modal=True,
                message_type=Gtk.MessageType.INFO,
                text=output, title="Search Result",
                buttons=("OK", Gtk.ResponseType.OK)
            )
            search_result_dialog.run()
            search_result_dialog.destroy()

        dialog.destroy()


    def search_and_mark(self, text, start):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match is not None:
            self.count += 1
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(text, match_end)


    def on_find_clicked(self, widget):
        dialog = FindReplaceDialog(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.APPLY:
            cursor_mark = self.textbuffer.get_insert()
            start = self.textbuffer.get_iter_at_mark(cursor_mark)
            
            if start.get_offset() == self.textbuffer.get_char_count():
                start = self.textbuffer.get_start_iter()

            self.find_and_replace(dialog.find_entry.get_text(), dialog.replace_entry.get_text(), start)

        elif response ==  Gtk.ResponseType.CANCEL:
            dialog.destroy()

        dialog.destroy()


    def find_and_replace(self, oldtext, newtext, start):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(oldtext, 0, end)

        if match is not None:
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
            self.textbuffer.delete(match_start, match_end)  
            self.textbuffer.insert(match_end, newtext, len(newtext))
            self.find_and_replace(oldtext, newtext, match_end)


    def on_editable_toggled(self, widget):
        self.textview.set_editable(widget.get_active())
    

    def on_cursor_toggled(self, widget):
        self.textview.set_cursor_visible(widget.get_active())


    def on_wrap_toggled(self, widget, mode):
        self.textview.set_wrap_mode(mode)


    def on_quit_clicked(self, button):
        dialog = Gtk.MessageDialog(
            title="Close Window", 
            parent=self, 
            modal=True
        )
        dialog.set_border_width(10)
        dialog.add_button("Yes", Gtk.ResponseType.YES)
        dialog.add_button("No", Gtk.ResponseType.NO)
        dialog.props.text = "Are you sure you want to exit?"
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            self.destroy()
        dialog.destroy()


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp", **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Lucid Text")
        self.window.show_all()
        self.window.present()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
