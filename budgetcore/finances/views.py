from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Bank, Category, Expense
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms  import ExpenseForm
import json

# Create your views here.
def banks_list(request):
    if request.method == 'DELETE':
        id = json.loads(request.body)['id']
        bank = get_object_or_404(Bank, id=id)
        bank.delete()
        
    bank_list = Bank.objects.all()
    return render(request, 'finances/bank_list.html', {'bank_list': bank_list})

def finance_info(request, bank_slug):
    bank = get_object_or_404(Bank, slug=bank_slug)

    if request.method == 'GET':
        category_list = Category.objects.filter(bank=bank)
        return render(request, 'finances/finance_info.html', {'bank': bank, 'expense_list': bank.expenses.all(), 'category_list': category_list})

    elif request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            category = get_object_or_404(Category, bank=bank, name=category_name)

            Expense.objects.create(
                bank=bank,
                title=title,
                amount=amount,
                category=category
            ).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(bank_slug)

class BankCreateView(CreateView):
    model = Bank
    template_name = 'finances/add-bank.html'
    fields = ('name', 'balance')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                bank=Bank.objects.get(id=self.object.id),
                name=category
            ).save()

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return slugify(self.request.POST['name'])
