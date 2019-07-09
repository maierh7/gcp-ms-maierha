package main

// BEFORE RUNNING:
// ---------------
// 1. If not already done, enable the Cloud SQL Administration API
//    and check the quota for your project at
//    https://console.developers.google.com/apis/api/sqladmin
// 2. This sample uses Application Default Credentials for authentication.
//    If not already done, install the gcloud CLI from
//    https://cloud.google.com/sdk/ and run
//    `gcloud beta auth application-default login`.
//    For more information, see
//    https://developers.google.com/identity/protocols/application-default-credentials
// 3. Install and update the Go dependencies by running `go get -u` in the
//    project directory.

import (
	"fmt"
	"log"

	"context"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/sqladmin/v1beta4"
)

func main() {
	ctx := context.Background()

	c, err := google.DefaultClient(ctx, sqladmin.CloudPlatformScope)
	if err != nil {
		log.Fatal(err)
	}

	sqladminService, err := sqladmin.New(c)
	if err != nil {
		log.Fatal(err)
	}

	// Project ID of the project that contains the instance.
	project := "v135-5256-playground-haraldmai"

	// Cloud SQL instance ID. This does not include the project ID.
	instance := "hm1-pg"

	// The ID of this Backup Run.
	id := int64(1562612402967)

	resp, err := sqladminService.BackupRuns.Get(project, instance, id).Context(ctx).Do()
	if err != nil {
		log.Fatal(err)
	}

	// TODO: Change code below to process the `resp` object:
	fmt.Printf("%#v\n", resp)
}
