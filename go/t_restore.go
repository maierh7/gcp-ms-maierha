
package main

import (
	"fmt"
	"log"
	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/sqladmin/v1beta4"
)

func main () {
	ctx := context.Background ()

	c, err := google.DefaultClient(ctx, sqladmin.CloudPlatformScope)

	if err != nil {
		log.Fatal (err)
	}

	sqladm, err := sqladmin.New (c)
	if err != nil {
		log.Fatal (err)
	}

	
	rb := &sqladmin.InstancesRestoreBackupRequest {
		RestoreBackupContext : &sqladmin.RestoreBackupContext {
			Kind        : "sql#restoreBackupContext",
			BackupRunId : 0,
			Project     : "",
			InstanceId  : "",
		},
	}

	_ = sqladm
	_ = rb
	
	fmt.Printf ("t_restore\n")
}
