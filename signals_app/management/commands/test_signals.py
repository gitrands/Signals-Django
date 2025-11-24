import time
import threading
from django.core.management.base import BaseCommand
from django.dispatch import Signal, receiver
from django.db import transaction
from signals_app.models import Log
from signals_app.rectangle import Rectangle

# Define signals
test_signal_1 = Signal()
test_signal_2 = Signal()
test_signal_3 = Signal()

class Command(BaseCommand):
    help = 'Runs tests to demonstrate Django signal behavior'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Signal Tests...'))
        
        # --- Question 1: Sync vs Async ---
        self.stdout.write(self.style.WARNING('\n--- Question 1: By default are django signals executed synchronously or asynchronously? ---'))
        
        @receiver(test_signal_1)
        def slow_receiver(sender, **kwargs):
            print("Receiver: Started processing...")
            time.sleep(2)
            print("Receiver: Finished processing.")

        start_time = time.time()
        print("Caller: Sending signal...")
        test_signal_1.send(sender=self.__class__)
        end_time = time.time()
        print(f"Caller: Signal sent. Total time taken: {end_time - start_time:.2f} seconds")
        
        if end_time - start_time >= 2:
            self.stdout.write(self.style.SUCCESS("Conclusion: Signals are synchronous by default (caller waited for receiver)."))
        else:
            self.stdout.write(self.style.SUCCESS("Conclusion: Signals are asynchronous."))

        # --- Question 2: Threads ---
        self.stdout.write(self.style.WARNING('\n--- Question 2: Do django signals run in the same thread as the caller? ---'))

        @receiver(test_signal_2)
        def thread_receiver(sender, **kwargs):
            print(f"Receiver: Running in thread: {threading.current_thread().name}")

        print(f"Caller: Running in thread: {threading.current_thread().name}")
        print("Caller: Sending signal...")
        test_signal_2.send(sender=self.__class__)
        
        self.stdout.write(self.style.SUCCESS("Conclusion: Signals run in the same thread as the caller by default."))

        # --- Question 3: Transactions ---
        self.stdout.write(self.style.WARNING('\n--- Question 3: By default do django signals run in the same database transaction as the caller? ---'))

        @receiver(test_signal_3)
        def db_receiver(sender, **kwargs):
            print("Receiver: Creating Log entry 'Signal Log'...")
            Log.objects.create(message="Signal Log")

        print("Caller: Initial Log count:", Log.objects.count())
        
        try:
            with transaction.atomic():
                print("Caller: Inside transaction. Creating Log entry 'Caller Log'...")
                Log.objects.create(message="Caller Log")
                print("Caller: Sending signal...")
                test_signal_3.send(sender=self.__class__)
                print("Caller: Raising exception to rollback transaction...")
                raise Exception("Force Rollback")
        except Exception as e:
            print(f"Caller: Caught exception: {e}")

        final_count = Log.objects.count()
        print(f"Caller: Final Log count: {final_count}")
        
        if final_count == 0:
            self.stdout.write(self.style.SUCCESS("Conclusion: Signals run in the same transaction (receiver's DB change was rolled back)."))
        else:
            self.stdout.write(self.style.SUCCESS("Conclusion: Signals run in a different transaction (receiver's DB change persisted)."))

        # --- Rectangle Class ---
        self.stdout.write(self.style.WARNING('\n--- Rectangle Class Demonstration ---'))
        rect = Rectangle(10, 5)
        print("Iterating over Rectangle(10, 5):")
        for item in rect:
            print(item)
