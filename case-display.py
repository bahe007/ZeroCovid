import helpers
import case_numbers

import matplotlib.pyplot as plt

############## Rohdaten ##############
file_name = helpers.todays_filename()
helpers.download_todays_data_if_needed()

############## Konstanten ##############
t, cases = case_numbers.get_cases(file_name)

############## Zeichne Fallzahlen ##############
fig, ax = plt.subplots()
xtick_positions = [t.index("2020/02/01"), t.index("2020/04/01"), t.index("2020/06/01"), t.index("2020/08/01"), t.index("2020/10/01"), t.index("2020/12/01")]
xlabels = ["Februar", "April", "Juni", "August", "Oktober", "Dezember"]
ax.set_xticks(xtick_positions)
ax.set_xticklabels(xlabels)

ax.grid(True)


ax.plot(t[:-3], helpers.moving_average(cases)[:-3])
plt.show()