~~ ΟΔΗΓΙΕΣ ΕΓΚΑΤΑΣΤΑΣΗΣ ΕΦΑΡΜΟΓΗΣ ~~

I)   Εγκατάσταση Python 3.x και mysql
  1. Λήψη της τελευταίας έκδοσης της Python 3.x (https://www.python.org/downloads/)
  2. Εγκατάσταση της Python 3.x (απαραίτητο να είναι ενεργοποιημένη η επιλογή "Add Python 3.x to PATH" αν γίνει εκτέλεση από τερματικό)
  3. Εγκατάσταση της βιβλιοθήκης mysql (https://pynative.com/install-mysql-connector-python/)

IΙ)  Εγκατάσταση XAMPP
  1. Λήψη του προγράμματος XAMPP (https://www.apachefriends.org/download.html)
  2. Εγκατάσταση του XAMPP (απαραίτητο να συμπεριληφθεί στην εγκατάσταση ο Apache server, MySQL και phpmyadmin)

III) Φόρτωμα βάσης δεδομένων busdb
  1. Εκτελέστε το XAMPP
  2. Στο control panel του XAMPP εκκινήστε τον Apache και την MySQL
  3. Στο ίδιο παράθυρο πατήστε το πλήκτρο Admin της MySQL
  4. Ο φυλλομετρητής θα ανοίξει την ιστοσελίδα localhost/phpmyadmin
  5. Στα αριστερά της οθόνης πατάμε το κουμπί new για να δημιουργήσουμε μια νέα βάση δεδομένων
  6. Δίνουμε όνομα busdb και στο ακριβώς δεξιά πεδίο επιλέγουμε utf8_general_ci και πατάμε create
  7. Επιλέγουμε από αριστερά τη βάση δεδομένων busdb και στο πάνω μέρος πατάμε import
  8. Επιλέγουμε το αρχείο busdb.sql και πατάμε go

