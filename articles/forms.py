from django import forms

from articles.models import Article, Comment

# class ArticleForm(forms.Form):
#     title = forms.CharField(min_length=5, max_length=100)
#     text = forms.Textarea()
#     rate = forms.IntegerField(min_value=0, max_value=10)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "text", "rate", "image", "category")

    def validation_title(self, title):
        if len(title) > 10:
            raise forms.ValidationError("validation error from func")

    def clean_title(self):
        title = self.cleaned_data["title"]

        if title == "NOT VALID":
            raise forms.ValidationError("TUT")

        self.validation_title(title)

        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

    BANNED_WORDS = [
    # оскорбления
    "дурак", "идиот", "тупой", "придурок", "дебил", "кретин",
    "тварь", "урод", "ничтожество", "мразь", "быдло", "лох",
    # спам и реклама
    "казино", "ставки", "букмекер", "займ", "кредит",
    "быстрый заработок", "крипта", "инвестиции", "раскрутка",
    "накрутка", "подписывайся", "переходи по ссылке",
    "пиши в телеграм", "скидка", "бесплатно", "выигрыш",
    # ссылки
    "http", "https", "www", ".ru", ".com", "t.me",]



    def clean_text(self):


        text = self.cleaned_data["text"]

        if len(text) < 5:
            raise forms.ValidationError("Текст комментария должен содержать минимум 5 символов.")

        text_lower = text.lower()
        for word in self.BANNED_WORDS:
            if word in text_lower:
                raise forms.ValidationError(f"Комментарий содержит запрещенное слово: «{word}».")
        
        return text


    