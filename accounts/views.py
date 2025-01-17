from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Company
from django.http import JsonResponse

def home(request):
    return render(request, 'accounts/home.html')

def get_step_template(step):
    templates = {
        1: 'accounts/steps/contact_info.html',
        2: 'accounts/steps/company_info.html',
        3: 'accounts/steps/transaction_info.html',
        4: 'accounts/steps/payment_info.html',
    }
    return templates.get(step, 'accounts/steps/contact_info.html')

@csrf_protect
def register_company(request):
    step = int(request.session.get('registration_step', 1))
    company_id = request.session.get('company_id')
    company = None

    if company_id:
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            company = None
            request.session['registration_step'] = 1
    
    if request.method == 'POST':
        try:
            if not company:
                company = Company()

            # Handle data based on current step
            if step == 1:  # Contact Information
                company.email = request.POST.get('email')
                company.full_name = request.POST.get('full_name')
                company.company_name = request.POST.get('company_name')
                company.country = request.POST.get('country')
                company.phone = request.POST.get('phone')
                company.save()
                request.session['company_id'] = company.id
                request.session['registration_step'] = 2
                return redirect('accounts:register_company')
            
            elif step == 2:  # Company Information
                company.legal_name = request.POST.get('legal_name')
                company.commercial_name = request.POST.get('commercial_name')
                company.state = request.POST.get('state')
                company.city = request.POST.get('city')
                company.postal_code = request.POST.get('postal_code')
                company.address = request.POST.get('address')
                company.website = request.POST.get('website')
                company.tax_id = request.POST.get('tax_id')
                company.start_date = request.POST.get('start_date')
                company.company_type = request.POST.get('company_type')
                company.save()
                request.session['registration_step'] = 3
                return redirect('accounts:register_company')
            
            elif step == 3:  # Transaction Information
                company.transaction_purpose = request.POST.get('transaction_purpose')
                company.annual_volume = request.POST.get('annual_volume')
                company.annual_transactions = request.POST.get('annual_transactions')
                company.currencies_needed = request.POST.get('currencies_needed')
                company.save()
                request.session['registration_step'] = 4
                return redirect('accounts:register_company')
            
            elif step == 4:  # Payment Method
                company.payment_method = request.POST.get('payment_method')
                if company.payment_method in ['ach', 'transfer']:
                    company.bank_name = request.POST.get('bank_name')
                    company.bank_address = request.POST.get('bank_address')
                    company.account_number = request.POST.get('account_number')
                    company.routing_number = request.POST.get('routing_number')
                    company.account_type = request.POST.get('account_type')
                company.is_completed = True
                company.save()
                
                # Clear session data after successful registration
                request.session.pop('registration_step', None)
                request.session.pop('company_id', None)
                messages.success(request, '¡Registro completado exitosamente!')
                return redirect('accounts:registration_complete')
                
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('accounts:register_company')
    
    template = get_step_template(step)
    context = {
        'step': step,
        'total_steps': 4,
        'company': company,
        'current_step': step
    }
    
    return render(request, template, context)

def registration_complete(request):
    return render(request, 'accounts/registration_complete.html')
