# README

A server sample of using the did-vc module. To walk through the example, launch the ganache chain with the seed `123`.

Then launch the server with

```sh
go run . --config sample_cfg.json
```

Interact with the client:

```sh
curl -X POST -H "Content-Type: application/json" -d @sample_create_issuer_did.json localhost:2592/create-did
curl -X POST -H "Content-Type: application/json" -d @sample_create_receiver_did.json localhost:2592/create-did
curl -X POST -H "Content-Type: application/json" -d @sample_register_cpt.json localhost:2592/register-cpt
curl -X POST -H "Content-Type: application/json" -d @sample_issue_vc.json localhost:2592/issue-vc
curl -X POST -H "Content-Type: application/json" -d @sample_verify_vc.json localhost:2592/verify-vc
```
