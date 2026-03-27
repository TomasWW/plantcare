from django.shortcuts import render,redirect, get_object_or_404
from apps.plants.models import Plant
from .forms import PlantForm
from .services import PlantAnalyzer
import logging

import json

logger = logging.getLogger(__name__)


def analyze_plant(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            try:
                analysis_result = PlantAnalyzer.analyze_plant(image)
                data = json.loads(analysis_result)
                request.session['plant_data'] = data
                return redirect('plant_confirm')
            except Exception as e:
                logger.error(f"Error occurred while analyzing plant: {str(e)}")
                form.add_error(None, "We couldn't analyze your plant. Please try again.")

        
        else:
            form.add_error(None, "Please upload a valid image.")
    else:
        form = PlantForm()
    return render(request, 'plants/analyze.html', {'form': form})

def plant_list(request):
    plants = Plant.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'plants/plant_list.html', {'plants': plants})
    

def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    return render(request, 'plants/plant_detail.html', {'plant': plant})

def plant_confirm(request):
    plant_data = request.session.get('plant_data')
    if not plant_data:
        return redirect('analyze_plant')
    if request.method == "POST":
        Plant.objects.create(
            user=request.user,
            scientific_name=plant_data.get('scientific_name', ''),
            common_name=plant_data.get('common_name', ''),
            care_data=plant_data.get('care_data', {})
        )
        del request.session['plant_data']
        return redirect('plant_list')
    return render(request, 'plants/plant_confirm.html', {'plant_data': plant_data})
