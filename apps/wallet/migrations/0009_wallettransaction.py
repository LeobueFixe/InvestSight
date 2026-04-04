from django.conf import settings
from django.db import migrations, models

# This migration adds the WalletTransaction model to track all transactions related to the user's wallet, including sends, receives, imports, and address creations. It also links each transaction to the user for easy retrieval and management.
class Migration(migrations.Migration):
    dependencies = [
        ("wallet", "0002_add_wallet"),
        ("wallet", "0008_remove_sensitive_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WalletTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("receive", "Receive"),
                            ("send", "Send"),
                            ("import", "Import"),
                            ("address", "New Address"),
                            ("security", "Security"),
                        ],
                        max_length=20,
                    ),
                ),
                ("asset_symbol", models.CharField(blank=True, max_length=12)),
                (
                    "amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=8,
                        max_digits=20,
                        null=True,
                    ),
                ),
                ("from_address", models.CharField(blank=True, max_length=255)),
                ("to_address", models.CharField(blank=True, max_length=255)),
                ("reference", models.CharField(blank=True, max_length=128)),
                ("note", models.CharField(blank=True, max_length=255)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="wallet_transactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
