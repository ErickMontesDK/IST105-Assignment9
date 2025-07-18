from django.db import models

# Modelo para guardar logs de acciones
class ActionLog(models.Model):
    actions = [
        ('authenticate', 'authenticate'),
        ('list_devices', 'list devices'),
        ('list_interfaces', 'list interfaces'),
    ]
    results = [
        ('success', 'success'),
        ('failure', 'failure')
    ]
    device_ip = models.CharField(max_length=45, null=True, blank=True)  # Soporta IPv6 y puede ser nulo
    action = models.CharField(max_length=20, choices=actions)
    result = models.CharField(max_length=10, choices=results)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: {self.action} ({self.device_ip})"