# from audioop import getsample
from django.http import HttpResponse
import this
from django.http import FileResponse
from paquete.models import paquete, tipoPaquete
from django.db.models import Sum, FloatField, Value
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reportlab.platypus import Table, TableStyle
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from django.utils import timezone
from report.api import serializable
from user.models import extencion
from utils.random import cbxtovalue,rgba

import calendar
from django.utils.translation import gettext as _


import base64
from django.template.loader import render_to_string
from weasyprint import HTML
from CSEPcon.settings import DIR, os


class reportPaquetesFecha(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serialize = serializable.Consult(data=request.data)
        if serialize.is_valid():
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4, bottomup=1)
            # Cabecera
            c.setLineWidth(.3)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(200, 800, "Reporte de entregas")
            c.setFont("Helvetica", 18)
            fecha = str(serialize["fecha_inicio"].value)
            c.drawString(30, 750, "Realizado el: " +
                         timezone.now().strftime("%d/%m/%Y"))
            c.drawString(30, 720, "Fecha de entregas: " + fecha)

            # Prueba tabla
            # tabla= ["#","Nombre"]
            # datos= [{"#":1,"Nombre":"Queso"}, {"#":2,"Nombre":"Leche"}, {"#":3,"Nombre":"Chocolate"}]
            # for x in datos:
            #     distabla= [x["#"], x["Nombre"]]
            #     tabla.append(distabla)
            # T= Table(tabla)
            # width, height= A4
            # T.wrapOn(c, width,height)
            # T.drawOn(c, 30, 630)
            tpaquetes = [["Codigo", "Repartidor",
                          "Cliente", "Estado", "Fecha", "Hora"]]
            rep = extencion.objects.get(usuario=request.user.id)
            total = paquete.objects.filter(
                repartidor=rep, paq_fechaConfirmacion=fecha).count()
            alto = 671
            for paq in paquete.objects.filter(repartidor=rep, paq_fechaConfirmacion=fecha):
                this_paq = [paq.paq_numero, paq.repartidor, paq.user, paq.paq_estado,
                            paq.paq_fechaConfirmacion, paq.paq_horaConfirmacion]
                tpaquetes.append(this_paq)
                alto -= 29
            if len(tpaquetes) > 1:
                T = Table(tpaquetes, inch*1.32, (total+1)*[0.4*inch])
                print((total+1)*-1)
                T.setStyle(TableStyle([('FONTNAME', (0, 0), (5, (total+1)*-1), "Helvetica-Bold"),
                                       ('SIZE', (0, 1), (5, -1), 12),  # Detalle
                                       # cabecera
                                       ('SIZE', (0, 0), (5, (total+1)*-1), 17),
                                       ('VALIGN', (0, 0), (5, -1), 'MIDDLE'),
                                       ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                                       ]))
                width, height = A4
                T.wrapOn(c, width, height)
                T.drawOn(c, 12, alto)
                # Crear archivo
                c.showPage()
                c.save()
                buf.seek(0)
                return FileResponse(buf, as_attachment=True, filename='reporte.pdf')
            else:
                return Response("No existe reportes en esa fecha", status=status.HTTP_404_NOT_FOUND)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
# Sin token


class reportPaquetesFechaNoToken(APIView):
    def post(self, request):
        serialize = serializable.Consult(data=request.data)
        if serialize.is_valid():
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4, bottomup=1)
            # Cabecera
            c.setLineWidth(.3)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(200, 800, "Reporte de entregas")
            c.setFont("Helvetica", 18)
            fecha = str(serialize["fecha_inicio"].value)
            c.drawString(30, 750, "Realizado el: " +
                         timezone.now().strftime("%d/%m/%Y"))
            c.drawString(30, 720, "Fecha de entregas: " + fecha)

            # Prueba tabla
            tpaquetes = [["Codigo", "Repartidor",
                          "Cliente", "Estado", "Fecha", "Hora"]]
            total = paquete.objects.filter(paq_fechaConfirmacion=fecha).count()
            alto = 671
            for paq in paquete.objects.filter(paq_fechaConfirmacion=fecha):
                this_paq = [
                    paq.paq_numero,
                    paq.repartidor,
                    paq.user,
                    paq.paq_estado,
                    paq.paq_fechaConfirmacion,
                    paq.paq_horaConfirmacion
                ]
                tpaquetes.append(this_paq)
                alto -= 29

            if len(tpaquetes) > 1:
                T = Table(tpaquetes, inch * 1.32, (total + 1) * [0.4 * inch])
                print((total + 1) * -1)
                T.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (5, (total + 1) * -1), "Helvetica-Bold"),
                    ('SIZE', (0, 1), (5, -1), 12),  # Detalle
                    ('SIZE', (0, 0), (5, (total + 1) * -1), 17),  # cabecera
                    ('VALIGN', (0, 0), (5, -1), 'MIDDLE'),
                    ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ]))
                width, height = A4
                T.wrapOn(c, width, height)
                T.drawOn(c, 12, alto)

                # Crear archivo
                c.showPage()
                c.save()
                buf.seek(0)
                return FileResponse(buf, as_attachment=True, filename='reporte.pdf')
            else:
                return Response("No existe reportes en esa fecha", status=status.HTTP_404_NOT_FOUND)

        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class reportPaquetesFechaConfirmacion(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serial = serializable.Filtro(data=request.data)
            if serial.is_valid():
                print(serial.validated_data)
                url = request.META.get('wsgi.url_scheme') + \
                    '://' + request.META.get('HTTP_HOST')
                base_media = f"{url}/media"
                info_paquete = paquete.objects.filter(
                    paq_fechaConfirmacion__gte=serial["fecha_inicio"].value, paq_fechaConfirmacion__lte=serial["fecha_fin"].value)
                if info_paquete.count() == 0:
                    return Response({"error": "No existe reportes en esa fecha"}, status=status.HTTP_404_NOT_FOUND)
                fechaCreacion= timezone.now()
                user=request.user
                context = {"url": url, "image": f"{base_media}/empresa/logo.png", "nombre_empresa": "CSEP Delivery", "paquete": info_paquete,
                           "fechaInicio": serial.validated_data.get("fecha_inicio"), "fechaFin": serial.validated_data.get("fecha_fin"),"fechaCreacion":fechaCreacion,"user":user}
                html_string = render_to_string(
                    'paquetes/paquetes.html', context)
                pdf_file = HTML(string=html_string).write_pdf()
                pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')
                folder = "media/reportes/fechaConfirmacion"
                if not os.path.exists(DIR + folder):
                    os.makedirs(DIR + folder)
                pdf_name = f"reporteFechaConfirmacion_{serial['fecha_inicio'].value}_{serial['fecha_fin'].value}.pdf"
                with open(f"{DIR}{folder}/{pdf_name}", "wb") as f:
                    f.write(pdf_file)
                urlFile = f"{url}/{folder}/{pdf_name}"
                return Response({"urlFile": urlFile, "pdf_base64": pdf_base64}, status=status.HTTP_200_OK)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class reportPaquetesRepartidor(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            serial = serializable.FiltroRepartidor(data=request.data)
            if serial.is_valid():
                repartidor_add = serial.validated_data.get("repartidor_add")
                if repartidor_add is None:
                    return Response({"error": "Falta el filtro del repartidor"}, status=status.HTTP_400_BAD_REQUEST)

                repartidor_id = cbxtovalue(repartidor_add)
                if repartidor_id is None:
                    return Response({"error": "El filtro del repartidor es inválido"}, status=status.HTTP_400_BAD_REQUEST)

                url = request.META.get('wsgi.url_scheme') + \
                    '://' + request.META.get('HTTP_HOST')
                base_media = f"{url}/media"

                info_paquete = paquete.objects.filter(repartidor=repartidor_id)

                if info_paquete.count() == 0:
                    return Response({"error": "No existen paquetes para el repartidor seleccionado"}, status=status.HTTP_404_NOT_FOUND)
                fechaCreacion= timezone.now()
                user=request.user
                context = {
                    "url": url,
                    "image": f"{base_media}/empresa/logo.png",
                    "nombre_empresa": "CSEP Delivery",
                    "paquete": info_paquete,
                    "fechaCreacion":fechaCreacion,
                    "user":user
                }

                html_string = render_to_string(
                    'paquetes/paquetes.html', context)
                pdf_file = HTML(string=html_string).write_pdf()
                pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')

                folder = "media/reportes/repartidor"
                if not os.path.exists(DIR + folder):
                    os.makedirs(DIR + folder)

                pdf_name = f"reporteRepartidor_{repartidor_id}.pdf"
                with open(f"{DIR}{folder}/{pdf_name}", "wb") as f:
                    f.write(pdf_file)

                urlFile = f"{url}/{folder}/{pdf_name}"

                return Response({"urlFile": urlFile, "pdf_base64": pdf_base64}, status=status.HTTP_200_OK)

            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class reportPaquetesUsuario(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serial = serializable.FiltroUsuario(data=request.data)
            if serial.is_valid():
                user_add = serial.validated_data.get("user_add")
                if user_add is None:
                    return Response({"error": "Falta el filtro del usuario"}, status=status.HTTP_400_BAD_REQUEST)

                user_id = cbxtovalue(user_add)
                if user_id is None:
                    return Response({"error": "El filtro del usuario es inválido"}, status=status.HTTP_400_BAD_REQUEST)

                url = request.META.get('wsgi.url_scheme') + \
                    '://' + request.META.get('HTTP_HOST')
                base_media = f"{url}/media"

                info_paquete = paquete.objects.filter(user=user_id)
                user=request.user


                if info_paquete.count() == 0:
                    return Response({"error": "No existen paquetes para el usuario seleccionado"}, status=status.HTTP_404_NOT_FOUND)
                fechaCreacion= timezone.now()
                context = {
                    "url": url,
                    "image": f"{base_media}/empresa/logo.png",
                    "nombre_empresa": "CSEP Delivery",
                    "paquete": info_paquete,
                    "fechaCreacion":fechaCreacion,
                    "user":user
                }

                html_string = render_to_string(
                    'paquetes/paquetes.html', context)
                pdf_file = HTML(string=html_string).write_pdf()
                pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')

                folder = "media/reportes/usuario"
                if not os.path.exists(DIR + folder):
                    os.makedirs(DIR + folder)

                pdf_name = f"reporteUsuario_{user_id}.pdf"
                with open(f"{DIR}{folder}/{pdf_name}", "wb") as f:
                    f.write(pdf_file)

                urlFile = f"{url}/{folder}/{pdf_name}"

                return Response({"urlFile": urlFile, "pdf_base64": pdf_base64}, status=status.HTTP_200_OK)

            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class chartEntregadosNoEntregados(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            serial= serializable.FiltroChart(data=request.data)
            if serial.is_valid():
                print(serial.validated_data.get("fecha_inicio"))
                if serial.validated_data.get("fecha_inicio") is None:
                    entregados= paquete.objects.filter(paq_estado="Entregado")
                    noEntregados= paquete.objects.filter(paq_estado="No entregado")
                else:
                    entregados= paquete.objects.filter(paq_estado="Entregado", paq_fechaConfirmacion__gte=serial.validated_data.get("fecha_inicio"), paq_fechaConfirmacion__lte=serial.validated_data.get("fecha_fin"))
                    noEntregados= paquete.objects.filter(paq_estado="No entregado", paq_fechaConfirmacion__gte=serial.validated_data.get("fecha_inicio"), paq_fechaConfirmacion__lte=serial.validated_data.get("fecha_fin")) 
                if serial.validated_data.get("usuario") is not None:
                    print(serial.validated_data.get("usuario").get("value"))
                    entregados=entregados.filter(user_id = serial.validated_data.get("usuario").get("value"))
                    noEntregados=noEntregados.filter(user_id = serial.validated_data.get("usuario").get("value"))
                total=entregados.count()+noEntregados.count()
                print(total)
                entregadoPorcentaje=entregados.count()*100/total
                noEntregadoPorcentaje=noEntregados.count()*100/total
                return Response([entregados.count() , noEntregados.count()], status=status.HTTP_200_OK)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class chartTipoPaquete(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            serial= serializable.FiltroChart(data=request.data)
            if serial.is_valid():
                tipos= tipoPaquete.objects.all()
                listaNombres=[]
                listaNumero=[]
                for tipo in tipos:
                    if serial.validated_data.get("fecha_inicio") is None:
                        paquete_count= paquete.objects.filter(paq_tip=tipo)
                        if serial.validated_data.get("usuario") is not None:
                            paquete_count= paquete_count.filter(user_id=serial.validated_data.get("usuario").get("value"))
                        print(paquete_count)
                        listaNumero.append(paquete_count.count())
                    else:
                        paquete_count= paquete.objects.filter(paq_tip=tipo, paq_fechaConfirmacion__gte=serial.validated_data.get("fecha_inicio"), paq_fechaConfirmacion__lte=serial.validated_data.get("fecha_fin"))
                        if serial.validated_data.get("usuario") is not None:
                            paquete_count= paquete_count.filter(user_id=serial.validated_data.get("usuario").get("value"))
                        listaNumero.append(paquete_count.count())
                    listaNombres.append(tipo.nombre)
                return Response([listaNombres, listaNumero], status=status.HTTP_200_OK)
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class chartPrecio(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            serial= serializable.FiltroChart(data=request.data)
            if serial.is_valid():
                listaAnio=[]
                listaMeses=[]
                listaMeses2=[]
                fecha_ant=""
                mes_ant=""
                datasets=[]
                if serial.validated_data.get("fecha_inicio") is None:
                    paquete_data= paquete.objects.all().order_by("paq_fechaCreacion")
                    if serial.validated_data.get("usuario") is not None:
                        paquete_data=paquete_data.filter(user_id=serial.validated_data.get("usuario").get("value"))
                    for data in paquete_data:
                        if not fecha_ant==data.paq_fechaCreacion.year:
                            jdata={
                             "label":data.paq_fechaCreacion.year,
                            }
                            listaAnio.append(jdata)
                        fecha_ant=data.paq_fechaCreacion.year
                        if not mes_ant==data.paq_fechaCreacion.month:
                            listaMeses2.append(data.paq_fechaCreacion.month)
                        mes_ant=data.paq_fechaCreacion.month
                    print(listaAnio)
                    listaMeses2.sort()
                    for mes in listaMeses2:
                            month_name = _(calendar.month_name[mes])
                            listaMeses.append(month_name)
                    for anio in listaAnio:
                        listaCostos=[]
                        for mes in listaMeses2:
                            suma_costo= paquete.objects.filter(paq_fechaCreacion__year=anio.get("label"),paq_fechaCreacion__month=mes)
                            if serial.validated_data.get("usuario") is not None:
                                suma_costo=suma_costo.filter(user_id=serial.validated_data.get("usuario").get("value"))
                            suma_costo=suma_costo.aggregate(total=Coalesce(Sum('paq_precio', output_field=FloatField()),Value(0, output_field=FloatField())))['total']
                            print(f"{anio} - {mes} - {suma_costo}")
                            listaCostos.append(suma_costo)
                        jdata={
                            "label":anio.get("label"),
                            "data":listaCostos,
                            "backgroundColor":rgba()
                        }
                        datasets.append(jdata)
                    print(datasets)
                    return Response({"labels":listaMeses,"datasets":datasets}, status=status.HTTP_200_OK)
                else:
                    paquete_data= paquete.objects.filter(paq_fechaCreacion__gte=serial.validated_data.get("fecha_inicio"),paq_fechaCreacion__lte=serial.validated_data.get("fecha_fin")).order_by("paq_fechaCreacion")
                    if serial.validated_data.get("usuario") is not None:
                        paquete_data=paquete_data.filter(user=serial.validated_data.get("usuario").get("value"))
                    for data in paquete_data:
                        if not fecha_ant==data.paq_fechaCreacion.year:
                            jdata={
                             "label":data.paq_fechaCreacion.year,
                            }
                            listaAnio.append(jdata)
                        fecha_ant=data.paq_fechaCreacion.year
                        if not mes_ant==data.paq_fechaCreacion.month:
                            listaMeses2.append(data.paq_fechaCreacion.month)
                        mes_ant=data.paq_fechaCreacion.month
                    print(listaAnio)
                    listaMeses2.sort()
                    for mes in listaMeses2:
                            month_name = _(calendar.month_name[mes])
                            listaMeses.append(month_name)
                    for anio in listaAnio:
                        listaCostos=[]
                        for mes in listaMeses2:
                            suma_costo= paquete.objects.filter(paq_fechaCreacion__year=anio.get("label"),paq_fechaCreacion__month=mes)
                            if serial.validated_data.get("usuario") is not None:
                                suma_costo=suma_costo.filter(user_id=serial.validated_data.get("usuario").get("value"))
                            suma_costo=suma_costo.aggregate(total=Coalesce(Sum('paq_precio', output_field=FloatField()),Value(0, output_field=FloatField())))['total']
                            print(f"{anio} - {mes} - {suma_costo}")
                            listaCostos.append(suma_costo)
                        jdata={
                            "label":anio.get("label"),
                            "data":listaCostos,
                            "backgroundColor":rgba()
                        }
                        datasets.append(jdata)
                    print(datasets)
                    return Response({"labels":listaMeses,"datasets":datasets}, status=status.HTTP_200_OK)
            return Response(serial.errors,status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


"""
class reportPaquetesFechaConfirmacion(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serial = serializable.Filtro(data=request.data)
            if serial.is_valid():
                print(serial.validated_data)
                url = request.META.get('wsgi.url_scheme') + '://' + request.META.get('HTTP_HOST')
                base_media = f"{url}/media"
                info_paquete = paquete.objects.filter(paq_fechaConfirmacion__gte=serial["fecha_inicio"].value, paq_fechaConfirmacion__lte=serial["fecha_fin"].value)
                if info_paquete.count() == 0:
                    return Response({"error": "No existe reportes en esa fecha"}, status=status.HTTP_404_NOT_FOUND)
                context = {"url": url, "image": f"{base_media}/empresa/logo.png", "nombre_empresa": "CSEP Delivery", "paquete": info_paquete, "fechaInicio": serial.validated_data.get("fecha_inicio"), "fechaFin": serial.validated_data.get("fecha_fin")}
                html_string = render_to_string('paquetes/paquetes.html', context)
                pdf_file = weasyprint.HTML(string=html_string).write_pdf()
                pdf_name = f"reporteFechaConfirmacion_{serial['fecha_inicio'].value}_{serial['fecha_fin'].value}.pdf"
                response = HttpResponse(pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'
                return response
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
"""
