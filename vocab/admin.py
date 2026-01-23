from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect

from .models import Word
from .sheets_sync import sync_words_from_sheets


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "translation", "example")
    search_fields = ("word", "translation", "example")

    # use our custom template to show the button
    change_list_template = "admin/vocab/word/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-from-sheets/",
                self.admin_site.admin_view(self.sync_from_sheets),
                name="vocab_word_sync_from_sheets",
            ),
        ]
        return custom_urls + urls

    def sync_from_sheets(self, request):
        try:
            stats = sync_words_from_sheets()
            messages.success(
                request,
                (
                    f"Synced from Sheets ✅ "
                    f"Rows: {stats['rows']} | "
                    f"Upserted: {stats['upserted']} | "
                    f"Skipped: {stats['skipped']}"
                ),
            )
        except Exception as e:
            messages.error(request, f"Sync failed ❌ {e}")
        return redirect("..")
