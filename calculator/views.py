from django.shortcuts import render
from django.views import View
from .forms import InvestmentForm

class Index(View):
    def get(self, request):
        # Render the form
        # Renders a unbounded form (empty form)
        form = InvestmentForm()

        context = {
            'form': form
        }

        return render(request, 'calculator/index.html', context)

    def post(self, request):
        # Takes POST request data from index.html

        # Getting access from form data sent through the POST request
        # Bounded form (Form filled with data)
        form = InvestmentForm(request.POST)

        if form.is_valid():
            total_result = form.cleaned_data['starting_amount']
            total_interest = 0
            yearly_results = {}

            for i in range(1, int(form.cleaned_data['number_of_years'] + 1)):
                yearly_results[i] = {}

                # calculate the interest
                interest = total_result * (form.cleaned_data['return_rate'] / 100)
                total_result += interest
                total_interest += interest

                # add additional contribution
                total_result += form.cleaned_data['annual_additional_contribution']

                # set the yearly_results
                yearly_results[i]['interest'] = round(total_interest, 2)
                yearly_results[i]['total'] = round(total_result, 2)

                # create context
                context = {
                    'total_result': round(total_result, 2),
                    'yearly_results': yearly_results,
                    'number_of_years': int(form.cleaned_data['number_of_years'])
                }

            # render the template
            return render(request, 'calculator/result.html', context)
