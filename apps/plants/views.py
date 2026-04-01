from django.shortcuts import render,redirect, get_object_or_404
from apps.plants.models import Plant
from .forms import PlantForm
from .services import PlantAnalyzer
import logging
import re
import json
from django.contrib.auth.decorators import login_required
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

@login_required
def analyze_plant(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            try:
                analysis_result = PlantAnalyzer.analyze_plant(image)
                json_match = re.search(r'\{.*\}', analysis_result, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                else:
                    raise ValueError("No JSON found in response")
                request.session['plant_data'] = data
                logger.debug(f"Plant data received: {data}  from analysis result: {analysis_result}")
                old_image_path  = request.session.get('plant_image')
                if old_image_path:
                    default_storage.delete(old_image_path)
                    del request.session['plant_image']
                image.seek(0)
                image_path = default_storage.save(f"temp/{image.name}", image)
                request.session['plant_image'] = image_path
                return redirect('plant_confirm')
            except Exception as e:
                logger.error(f"Error occurred while analyzing plant: {str(e)}")
                form.add_error(None, "We couldn't analyze your plant. Please try again.")
        
        else:
            form.add_error(None, "Please upload a valid image.")
    else:
        form = PlantForm()
    return render(request, 'plants/analyze.html', {'form': form})

@login_required
def plant_list(request):
    plants = Plant.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'plants/plant_list.html', {'plants': plants})
    
@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    return render(request, 'plants/plant_details.html', {'plant': plant})

@login_required
def plant_confirm(request):
    plant_data = request.session.get('plant_data')
    if not plant_data:
        return redirect('analyze_plant')
    if request.method == "POST":
        image_path = request.session.get('plant_image')
        if image_path:
            with default_storage.open(image_path, 'rb') as f:
                image_content = ContentFile(f.read(), name=os.path.basename(image_path))
        else:
            image_content = None
        Plant.objects.create(
            user=request.user,
            image=image_content,
            scientific_name=plant_data.get('scientific_name', ''),
            common_name=plant_data.get('common_name', ''),
            care_data=plant_data.get('care_data', {})
        )
        if image_path:
            default_storage.delete(image_path)
        del request.session['plant_data']
        del request.session['plant_image']
        return redirect('plant_list')
    return render(request, 'plants/plant_confirm.html', {'plant_data': plant_data})


@login_required
def plant_discard(request):
    image_path = request.session.get('plant_image')
    if image_path:
        default_storage.delete(image_path)
        del request.session['plant_image']
    if 'plant_data' in request.session:
        del request.session['plant_data']
    return redirect('analyze_plant')

@login_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    if request.method == "POST":
        if plant.image:
            default_storage.delete(plant.image.name)
        plant.delete()
        return redirect('plant_list')
    return render(request, 'plants/plant_delete_confirm.html', {'plant': plant})