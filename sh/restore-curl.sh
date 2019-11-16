#! /bin/bash

# gcloud auth login
ACCESS_TOKEN="$(gcloud auth print-access-token)"
curl   --header "Authorization: Bearer ${ACCESS_TOKEN}" \
       --header 'Content-Type: application/json' \
       --data '{
                  "restoreBackupContext":
                  {
                    "backupRunId": "1573540803091",
                    "project": "v135-5256-playground-haraldmai",
                    "instanceId": "hm1-pg"
                  }
                }' \
       -X POST      https://www.googleapis.com/sql/v1beta4/projects/xbbcvpbxkziv/instances/hm1-pg-ysys/restoreBackup
