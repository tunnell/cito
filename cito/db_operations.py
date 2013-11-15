# cito - The Xenon1T experiments software trigger
# Copyright 2013.  All rights reserved.
# https://github.com/tunnell/cito
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of the Xenon experiment, nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Commands for the command line interface for DB operations.
"""

import logging
from bson.code import Code

from cito.core import XeDB
from cito.base import CitoShowOne




class DBReset(CitoShowOne):

    """Reset the database by dropping the default collection.

    Warning: this cannot be used during a run as it will kill the DAQ writer.
    """

    def take_action(self, parsed_args):
        conn, db, collection = XeDB.get_mongo_db_objects(parsed_args.hostname)

        # The pymongo call
        db.drop_collection(collection.name)

        # TODO: Maybe purge celery too?
        #from celery.task.control import discard_all
        # discard_all()

        return self.get_status(db)


class DBPurge(CitoShowOne):

    """Delete/purge all DAQ documents without deleting collection.

    This can be used during a run.
    """

    def take_action(self, parsed_args):
        conn, db, collection = XeDB.get_mongo_db_objects(parsed_args.hostname)

        self.log.debug("Purging all documents")
        # The pymongo call
        collection.remove({})

        return self.get_status(db)


class DBRepair(CitoShowOne):

    """Repair DB to regain unused space.

    MongoDB can't know how what to do with space after a document is deleted,
    so there can exist small blocks of memory that are too small for new
    documents but non-zero.  This is called fragmentation.  This command
    copies all the data into a new database, then replaces the old database
    with the new one.  This is an expensive operation and will slow down
    operation of the database.
    """

    def take_action(self, parsed_args):
        conn, db, collection = XeDB.get_mongo_db_objects(parsed_args.hostname)

        # The actual pymongo call
        db.command('repairDatabase')

        return self.get_status(db)


class DBCount(CitoShowOne):

    """Count docs in DB.
    """

    def take_action(self, parsed_args):
        conn, db, collection = XeDB.get_mongo_db_objects(parsed_args.hostname)

        columns = ['Number of documents']
        data = [collection.count()]

        return columns, data


class DBDuplicates(CitoShowOne):

    """Find duplicate data and print their IDs.

    Search through all the DAQ document's data payloads (i.e., 'data' key) and
    if any of these are identical, list the keys so they can be inspected with
    the document inspector.  A Map-Reduce algorithm is used so the results are
    stored in MongoDB as the 'dups' collection.
    """

    def take_action(self, parsed_args):
        conn, db, collection = XeDB.get_mongo_db_objects(parsed_args.hostname)

        map_func = Code("function () {"
                        "  emit(this.data, 1); "
                        "}")

        reduce_func = Code("function (key, values) {"
                           "return Array.sum(values);"
                           "}")

        # Data to return
        columns = []
        data = []

        result = collection.map_reduce(map_func, reduce_func, "dups")
        for i, doc in enumerate(result.find({'value': {'$gt': 1}})):
            columns.append('Dup[%d] count' % i)
            data.append(doc['value'])

            for j, doc2 in enumerate(collection.find({'data': doc['_id']})):
                columns.append('Dup[%d][%d] ID' % (i, j))
                data.append(doc2['_id'])

        if len(columns):
            columns = ['Status'] + columns
            data = ['Duplicates found'] + data
        else:
            columns = ['Status']
            data = ['No duplicates']

        return columns, data
