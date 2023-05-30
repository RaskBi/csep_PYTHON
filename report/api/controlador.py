#from audioop import getsample
import this
from django.http import FileResponse
from paquete.models import paquete
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
class reportPaquetesFecha(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self, request):
        serialize= serializable.Consult(data=request.data)
        if serialize.is_valid():    
            buf= io.BytesIO()
            c= canvas.Canvas(buf, pagesize= A4, bottomup= 1)
            #Cabecera
            c.setLineWidth(.3)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(200, 800, "Reporte de entregas")
            c.setFont("Helvetica", 18)
            fecha=str(serialize["fecha_inicio"].value)
            c.drawString(30, 750,"Realizado el: "+ timezone.now().strftime("%d/%m/%Y"))
            c.drawString(30, 720,"Fecha de entregas: "+ fecha )
            
            #Prueba tabla
            # tabla= ["#","Nombre"]
            # datos= [{"#":1,"Nombre":"Queso"}, {"#":2,"Nombre":"Leche"}, {"#":3,"Nombre":"Chocolate"}]
            # for x in datos:
            #     distabla= [x["#"], x["Nombre"]]
            #     tabla.append(distabla)
            # T= Table(tabla)
            # width, height= A4
            # T.wrapOn(c, width,height)
            # T.drawOn(c, 30, 630)
            tpaquetes= [["Codigo", "Repartidor", "Cliente", "Estado", "Fecha", "Hora"]]
            rep=extencion.objects.get(usuario=request.user.id)
            total=paquete.objects.filter(repartidor=rep,paq_fechaConfirmacion=fecha).count()
            alto = 671
            for paq in paquete.objects.filter(repartidor=rep,paq_fechaConfirmacion=fecha):
                this_paq= [paq.paq_numero, paq.repartidor, paq.user, paq.paq_estado, paq.paq_fechaConfirmacion, paq.paq_horaConfirmacion]
                tpaquetes.append(this_paq)
                alto -= 29
            if len(tpaquetes)> 1:    
                T= Table(tpaquetes,inch*1.32, (total+1)*[0.4*inch])
                print((total+1)*-1)
                T.setStyle(TableStyle([('FONTNAME',(0,0), (5,(total+1)*-1),"Helvetica-Bold"),
                                        ('SIZE',(0,1), (5,-1),12),#Detalle
                                        ('SIZE',(0,0), (5,(total+1)*-1),17),#cabecera
                                        ('VALIGN', (0,0), (5,-1), 'MIDDLE'),
                                        ('GRID',(0,0),(-1,-1),1,(0,0,0)),
                                        ]))
                width, height= A4
                T.wrapOn(c, width,height)
                T.drawOn(c, 12, alto)
                #Crear archivo
                c.showPage()
                c.save()
                buf.seek(0)
                return FileResponse(buf, as_attachment= True, filename= 'reporte.pdf')
            else:
                return Response("No existe reportes en esa fecha",status=status.HTTP_404_NOT_FOUND)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
            