from django.db import migrations

# This migration removes the sensitive fields from the SeedPhrase and PrivateKey models.
class Migration(migrations.Migration):
    dependencies = [
        ("wallet", "0007_seedphrase_phrase"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="seedphrase",
            name="_phrase",
        ),
        migrations.RemoveField(
            model_name="privatekey",
            name="_private_key_value",
        ),
    ]
