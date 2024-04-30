Somchai Daniel Kanyavimonh
DMACC INTRO TO DATA STRUCTURES

Hello! Inside this folder you should find 3 files, The internal code for most of the methods and data structure creation called "DataStructuresFinal". The GUI itself called "FinalGUI" There is also the unit tests attached as well to cover scenarios.

HOW TO RUN
You'll launch the "FinalGUI" to get started. You'll have 3 overhead buttons in order they; let you place an order on a patient ID with user input, process the lab queue with the first order in line, or to generate a patient with random tests to speed up allocating the queue.

The first window below the 3 buttons is your patient queue, once orders are placed they are set to update and show in queue for in the window mentioned. It is set to update every second and is a priority queue. So if an order is placed STAT it will be placed in the queue infront of all othere tests that are not STAT. The queue will not if there are no supplies. For this finals sake, it is based upon if there are tubes avaiable for that test.

The second window is the current stock list, or what you have in your inventory on hand. Much like the patient queue window it is set to update every second. You have 2 buttons, to sort your supplies and to order supplies. Ordering supplies will open another window to select which test supplies you are ordering, they are set to provide a random expiration date and a random amount recieved. Once you have ordered an adequate amount of stock, it only makes sense to sort them by earliest expiration date and use that first to avoid wasting supplies. Sort Supplies button will organize the list with what has been recieved so far. It MUST be ran every time new stock is recieved prior to processing lab orders.