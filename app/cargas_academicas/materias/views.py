from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Materia, UnidadAcademica, ProgramaAcademico
from .forms import FormMateria, FormUnidadAcademica, FormProgramaAcademimco, FormFiltrosProgramaAcademico


@login_required
def home(request):
    return render(request, 'home.html')


class ProgramaDeleteView(DeleteView):
    model = ProgramaAcademico
    success_url = reverse_lazy('lista_programas')

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, 'Se eliminó el programa académico')
        except ProgramaAcademico.DoesNotExist:
            messages.error(
                self.request, 'No se pudo eliminar el programa académico')
        return redirect(success_url)


class ProgramaUpdateView(UpdateView):
    model = ProgramaAcademico
    extra_context = {
        'etiqueta_titulo': 'Actualizar programa académico',
        'etiqueta_boton': 'Guardar',
    }
    # fields = '__all__'
    form_class = FormProgramaAcademimco

    success_url = reverse_lazy('lista_programas')  # /materias/lista-materias


class ProgramaCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'materias.add_materia'
    model = ProgramaAcademico
    extra_context = {
        'etiqueta_titulo': 'Crear programa académico',
        'etiqueta_boton': 'Agregar',
    }
    # fields = '__all__'
    form_class = FormProgramaAcademimco
    success_url = reverse_lazy('lista_programas')  # /materias/lista-materias
    # form_class =


def lista_programas_filter(request):
    programas = ProgramaAcademico.objects.all().order_by('-nombre')
    form = FormFiltrosProgramaAcademico()
    if request.method == 'POST':
        form = FormFiltrosProgramaAcademico(request.POST)

        nombre = request.POST.get('nombre', None)
        unidad_academica = request.POST.get('unidad_academica', None)
        abreviacion = request.POST.get('abreviacion', None)
        if nombre:
            # programas = programas.filter(nombre__startswith = nombre)
            # programas = programas.filter(nombre__endswith = nombre)
            programas = programas.filter(nombre__contains=nombre)
        if unidad_academica:
            programas = programas.filter(
                unidad_academica__nombre__contains=unidad_academica)
            print(programas.query)
        if abreviacion:
            programas = programas.filter(abreviacion__contains=abreviacion)

    # print(programas.query)

    paginator = Paginator(programas, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list': page_obj,
        'form': form
    }
    return render(request, 'materias/programaacademico_list.html', context)


class ProgramasListView(ListView):
    model = ProgramaAcademico
    extra_context = {
        'form': FormFiltrosProgramaAcademico()
    }

    def get_queryset(self):
        print(self.request)
        if self.queryset is not None:
            queryset = self.queryset
            queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()

        # ordering = self.get_ordering()
        # if ordering:
        #     if isinstance(ordering, str):
        #         ordering = (ordering,)
        #     queryset = queryset.order_by(*ordering)
        return queryset


def editar_unidad(request, id):
    unidad = UnidadAcademica.objects.get(id=id)
    form = FormUnidadAcademica(instance=unidad)
    if request.method == 'POST':
        form = FormUnidadAcademica(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect('lista_unidades')
    context = {
        'form': form,
        'etiqueta_titulo': 'Modificar',
        'etiqueta_boton': 'Actualizar',
    }
    return render(request, 'nueva_unidad.html', context)


def eliminar_unidad(request, id):
    UnidadAcademica.objects.get(id=id).delete()
    return redirect('lista_unidades')


def nueva_unidad(request):
    form = FormUnidadAcademica()
    if request.method == 'POST':
        form = FormUnidadAcademica(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_unidades')
    context = {
        'form': form,
        'etiqueta_titulo': 'Nueva',
        'etiqueta_boton': 'Agregar',
    }
    return render(request, 'nueva_unidad.html', context)


def lista_unidades(request):
    unidades_academicas = UnidadAcademica.objects.all()
    # select * from unidadadacademica;
    context = {
        'unidades': unidades_academicas
    }
    return render(request, 'lista_unidades.html', context)


def nueva(request):
    form = FormMateria()
    context = {
        'form': form
    }
    return render(request, 'nueva_materia.html', context)


def eliminar(request, clave):
    Materia.objects.get(clave=clave).delete()
    return redirect('lista_materias')


def lista(request):
    context = {
        'materias': Materia.objects.all()
    }
    return render(request, 'materias.html', context)
