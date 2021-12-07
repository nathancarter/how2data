
#
# Run this script if you want to check which tasks belong to which topics,
# and whether any tasks are unattached to any topic.
# This is useful for ensuring that all tasks are in the database for a purpose.
#
# Usage:  python topic-check.py
#

import pandas as pd
from build_tools import *

# Start a new DataFrame containing just the names of all tasks:
report_df = pd.DataFrame( { 'task name' : tasks_df['task name'] } )

# For each task, compute the list of topics it appears in...
report_df['topics'] = report_df['task name'].apply( lambda name: \
    list( topics_df[topics_df['content'].str.contains( name, regex=False )]['topic name'] ) )
# ...and how many such topics there were in each case:
report_df['num topics'] = report_df['topics'].apply( len )

# Reorder rows and columns for readability/convenience:
report_df = report_df[['task name','num topics','topics']]
report_df = report_df.sort_values( by='num topics', ascending=False )

# Print the results to the console, with no truncation of any kind:
pd.set_option( 'display.max_rows', None )
pd.set_option( 'display.max_columns', None )
pd.set_option( 'display.width', None )
pd.set_option( 'display.max_colwidth', -1 )
print( report_df )
