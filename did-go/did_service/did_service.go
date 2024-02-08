package didservice

import (
	"context"
	"crypto/ecdsa"
	"encoding/hex"
	"errors"
	"fmt"
	"log"
	"math/big"
	"meca_did/common"
	"meca_did/constant"
	"meca_did/contract/did"
	"strconv"
	"strings"
	"time"

	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	ethcommon "github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/crypto"
	"github.com/ethereum/go-ethereum/ethclient"
)

var (
	STOP_RESOLVE_BLOCK_NUMBER = uint64(0)
)

type CreateDIDDataResult struct {
	Did string
	// PublicKey  string
	PublicKey  string
	PrivateKey string
}

type CreateDIDResponse struct {
	CreateDIDDataResult
	common.ServiceResponseInfo
}

type SetAuthenticationResponse struct {
	Success bool
	common.ServiceResponseInfo
}

type DidExistResponse struct {
	Exist bool
	common.ServiceResponseInfo
}

type DidDocumentResponse struct {
	Doc DidDocument
	common.ServiceResponseInfo
}

type DidDocumentJsonResponse struct {
	Doc string
	common.ServiceResponseInfo
}

type SetAttributeResponse struct {
	Success bool
	common.ServiceResponseInfo
}

type RevokePublicKeyWithAuthResponse SetAttributeResponse

type RevokeAuthResponse SetAttributeResponse

type AddPublicKeyResponse struct {
	Val int
	common.ServiceResponseInfo
}

type GetDidCountResponse struct {
	Count uint64
	common.ServiceResponseInfo
}

type DidService interface {
	Init() error
	CreateDID(publicKey string) (CreateDIDResponse, error)                                                // used
	SetAuthentication(did string, owner string, ownerPublicKey string) (SetAuthenticationResponse, error) // not used
	DidExist(did string) (DidExistResponse, error)                                                        // used
	GetDIDDocument(did string) (DidDocumentResponse, error)
	GetDIDDocumentJson(did string) (DidDocumentJsonResponse, error)
	RevokePublicKeyWithAuth(did string, keyType string, owner string, ownerPublicKey string, privateKey string) (RevokePublicKeyWithAuthResponse, error)
	RevokeAuthentication(did string, owner string, ownerPublicKey string, privateKey string) (RevokeAuthResponse, error)
	AddPublicKey(did string, keyType string, owner string, publicKey string, privateKey string) (AddPublicKeyResponse, error)
	GetDIDCount() (GetDidCountResponse, error)
}

var _ DidService = (*DidServiceImpl)(nil)

type DidServiceImpl struct {
	client                     *ethclient.Client
	contractAddr               string
	contractOwnerPrivateKeyStr string

	contract                *did.Did
	chainId                 *big.Int
	contractOwnerPrivateKey *ecdsa.PrivateKey
	contractOwnerAddr       ethcommon.Address
}

func NewDidService(client *ethclient.Client, contractAddr string, contractOwnerPrivateKeyStr string) *DidServiceImpl {
	return &DidServiceImpl{
		client:                     client,
		contractAddr:               contractAddr,
		contractOwnerPrivateKeyStr: contractOwnerPrivateKeyStr,
	}
}

func (s *DidServiceImpl) Init() error {
	if chainId, err := s.client.ChainID(context.Background()); err != nil {
		return err
	} else if contract, err := did.NewDid(ethcommon.HexToAddress(s.contractAddr), s.client); err != nil {
		return err
	} else if contractOwnerPrivateKey, err := crypto.HexToECDSA(s.contractOwnerPrivateKeyStr); err != nil {
		return err
	} else {
		s.chainId = chainId
		s.contract = contract
		s.contractOwnerPrivateKey = contractOwnerPrivateKey
		s.contractOwnerAddr = crypto.PubkeyToAddress(contractOwnerPrivateKey.PublicKey)
	}
	return nil
}

// TODO need to check if it is the right conversion

func LoadPublicKey(publicKey string) (*ecdsa.PublicKey, error) {
	bytes := make([]byte, hex.DecodedLen(len(publicKey)))
	_, err := hex.Decode(bytes, []byte(publicKey))
	if err != nil {
		return nil, err
	}
	pub, err := crypto.UnmarshalPubkey(bytes)
	if err != nil {
		return nil, err
	}
	return pub, nil
}

func (s *DidServiceImpl) prepareContractAuth() (*bind.TransactOpts, error) {
	auth, err := bind.NewKeyedTransactorWithChainID(s.contractOwnerPrivateKey, s.chainId)
	if err != nil {
		return nil, err
	}
	nonce, err := s.client.PendingNonceAt(context.Background(), s.contractOwnerAddr)
	if err != nil {
		return nil, err
	}
	gasPrice, err := s.client.SuggestGasPrice(context.Background())
	if err != nil {
		return nil, err
	}
	auth.Nonce = big.NewInt(int64(nonce))
	auth.Value = big.NewInt(0)
	auth.GasPrice = gasPrice
	auth.GasLimit = uint64(3000000)

	return auth, nil
}

func (s *DidServiceImpl) WaitForTxnCommit(tx *types.Transaction) (*types.Receipt, error) {
	ctx := context.Background()
	receipt, err := bind.WaitMined(ctx, s.client, tx)
	if err != nil {
		return nil, err
	}
	if receipt.Status != types.ReceiptStatusSuccessful {
		return nil, fmt.Errorf("transaction failed")
	}
	return receipt, nil
}

func (s *DidServiceImpl) CreateDID(publicKey string) (CreateDIDResponse, error) {
	resp := CreateDIDResponse{}
	resp.PublicKey = publicKey

	// get public key from address
	if len(publicKey) == 0 {
		resp.ErrCode = constant.DID_PUBLIC_KEY_LENGTH_INVALID
		return resp, nil
	}

	// get address from public key
	publicK, err := LoadPublicKey(publicKey)
	if err != nil {
		resp.ErrCode = constant.DID_PUBLICKEY_INVALID
		return resp, nil
	}
	address := crypto.PubkeyToAddress(*publicK)

	// check did exist
	targetDid := common.ConvertAddressToDID(address.Hex())
	log.Printf("targetDid: {%v}", targetDid)
	resp.Did = targetDid
	if existResp, err := s.DidExist(targetDid); err != nil {
		resp.ErrCode = constant.UNKNOW_ERROR
		return resp, nil
	} else if existResp.Exist {
		resp.ErrCode = constant.DID_ALREADY_EXIST
		return resp, nil
	} else {
		log.Printf("response did exist: {%v}", existResp)
	}

	// create did
	auth, err := s.prepareContractAuth()
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	didAuthVal := fmt.Sprintf("%s|%s", publicKey, address)
	created := fmt.Sprintf("%v", time.Now().UnixMilli())

	log.Printf("auth: {%v}", didAuthVal)
	log.Printf("created: {%v}", created)

	tx, err := s.contract.CreateDID(auth, address, []byte(didAuthVal), []byte(created), big.NewInt(time.Now().UnixMilli()))
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}
	receipt, err := s.WaitForTxnCommit(tx)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	blockNumber := receipt.BlockNumber.Uint64()
	it, err := s.contract.FilterDIDAttributeChanged(&bind.FilterOpts{Start: blockNumber, End: nil}, []ethcommon.Address{address})
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	ac := ReadDIDAttributeChangedEvent(it)
	if len(ac) == 0 {
		log.Fatal("DIDAttributeChangedEvent is empty")
		resp.ErrCode = constant.UNKNOW_ERROR
		return resp, nil
	}

	resp.TxInfo.SetTxInfo(receipt)
	return resp, nil
}

func (s *DidServiceImpl) SetAuthentication(did string, owner string, publicKey string) (SetAuthenticationResponse, error) {
	resp := SetAuthenticationResponse{}
	// todo input validation

	// check if did exist
	existResp, err := s.DidExist(did)
	if err != nil {
		resp.ErrCode = constant.UNKNOW_ERROR
		return resp, nil
	}
	if !existResp.Exist {
		resp.ErrCode = constant.DID_DOES_NOT_EXIST
		return resp, nil
	}

	// convert did to address
	address := ethcommon.HexToAddress(common.ConvertDIDToAddress(did))

	// prepare contract auth
	auth, err := s.prepareContractAuth()
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	// prepare arguments
	updated := big.NewInt(time.Now().UnixMilli())
	attrValue := []byte(fmt.Sprintf("%s|%s", publicKey, owner))
	var attrKey [32]byte
	copy(attrKey[:], []byte(constant.DID_DOC_AUTHENTICATE_PREFIX))

	tx, err := s.contract.SetAttribute(auth, address, attrKey, attrValue, updated)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	receipt, err := s.WaitForTxnCommit(tx)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	blockNumber := receipt.BlockNumber.Uint64()
	it, err := s.contract.FilterDIDAttributeChanged(&bind.FilterOpts{Start: blockNumber, End: nil}, []ethcommon.Address{address})
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	ac := ReadDIDAttributeChangedEvent(it)
	if len(ac) == 0 {
		log.Fatal("DIDAttributeChangedEvent is empty")
		resp.ErrCode = constant.DID_PRIVATEKEY_DOES_NOT_MATCH
		return resp, nil
	}
	resp.Success = true
	resp.TxInfo.SetTxInfo(receipt)
	return resp, nil
}

func (s *DidServiceImpl) DidExist(did string) (DidExistResponse, error) {
	resp := DidExistResponse{}
	address := ethcommon.HexToAddress(common.ConvertDIDToAddress(did))
	log.Printf("address: {%v}", address)
	exist, err := s.contract.IdentityExists(nil, address)
	log.Printf("did %v exist: {%v}", did, exist)
	log.Printf("err: {%v}", err)
	if err != nil {
		resp.ErrCode = constant.UNKNOW_ERROR
		return resp, errors.New("failed to check if did exist")
	}
	resp.Exist = exist
	resp.ErrCode = constant.SUCCESS
	return resp, nil
}

// add the attribute to the document
func constructDIDAttribute(attrKey, attrValue, did string, doc *DidDocument) {
	if strings.HasPrefix(attrKey, constant.DID_DOC_PUBLICKEY_PREFIX) {
		log.Printf("construct did pubkey %v, %v, %v, %v", attrKey, attrValue, did, doc)
		// construct did public keys
		publicKeyType := constant.DID_PUBLICKEY_TYPE_SECP256K1
		keyArray := strings.Split(attrKey, "/")
		if len(keyArray) > 2 {
			publicKeyType = keyArray[2]
		}

		// get revocation status
		isRevoked := strings.Contains(attrValue, constant.REMOVED_PUBKEY_TAG)
		trimmedPubKey := strings.Split(strings.Replace(attrValue, constant.REMOVED_PUBKEY_TAG, "", -1), "|")[0]
		for i, pk := range doc.PublicKey {
			if strings.Contains(pk.PublicKey, trimmedPubKey) {
				if !pk.Revoked == isRevoked {
					doc.PublicKey[i].Revoked = isRevoked
				}
				address := strings.Split(attrValue, "|")[1]
				owner := common.ConvertAddressToDID(address)
				doc.PublicKey[i].Owner = owner
				return
			}
		}

		if isRevoked {
			log.Fatalf("failed to revoke a non-existent public key %v from current document %v", attrValue, doc)
			return
		}
		pubKey := PublicKeyProperty{
			Id:   fmt.Sprintf("%s#keys-%d", did, len(doc.PublicKey)),
			Type: publicKeyType,
		}
		publicKeyData := strings.Split(attrValue, "|")
		if len(publicKeyData) == 2 {
			pubKey.PublicKey = publicKeyData[0]
			address := publicKeyData[1]
			owner := common.ConvertAddressToDID(address)
			pubKey.Owner = owner
		}
		doc.PublicKey = append(doc.PublicKey, pubKey)
	} else if strings.HasPrefix(attrKey, constant.DID_DOC_AUTHENTICATE_PREFIX) {
		log.Printf("construct did auth %v, %v, %v, %v", attrKey, attrValue, did, doc)
		// construct did authentication
		isRevoked := strings.Contains(attrValue, constant.REMOVED_AUTHENTICATION_TAG)
		for _, auth := range doc.Authentication {
			pubKeyId := auth.PublicKey
			for i, pk := range doc.PublicKey {
				if (pk.Id == pubKeyId) && strings.Contains(attrValue, pk.PublicKey) {
					if !auth.Revoked == isRevoked {
						doc.Authentication[i].Revoked = isRevoked
					}
					return
				}
			}
		}

		if isRevoked {
			log.Fatalf("failed to revoke a non-existent authentication %v from current document %v", attrValue, doc)
			return
		}
		for _, pk := range doc.PublicKey {
			if strings.Contains(attrValue, pk.PublicKey) {
				for _, auth := range doc.Authentication {
					if auth.PublicKey == pk.Id {
						return
					}
				}

				auth := AuthenticationProperty{
					PublicKey: pk.Id,
				}
				doc.Authentication = append(doc.Authentication, auth)
				return
			}
		}
	} else if strings.HasPrefix(attrKey, constant.DID_DOC_SERVICE_PREFIX) {
		// construct did service
		log.Printf("construct did service %v, %v, %v, %v", attrKey, attrValue, did, doc)
		service := strings.Split(attrKey, "/")[2]
		for i, s := range doc.Service {
			if s.Type == service {
				doc.Service[i].ServiceEndpoint = attrValue
				return
			}
		}
		s := ServiceProperty{
			Type:            service,
			ServiceEndpoint: attrValue,
		}
		doc.Service = append(doc.Service, s)
	} else {
		// construct did custom attribute
		log.Printf("construct did custom %v, %v, %v, %v", attrKey, attrValue, did, doc)
		if strings.Trim(attrKey, " ") == constant.DID_DOC_CREATED {
			// convert attrvalue string to uint64
			if created, err := strconv.ParseUint(attrValue, 10, 64); err != nil {
				log.Fatal("failed to convert created time to uint64")
			} else {
				doc.Created = created
			}
		}
	}
}

func (s *DidServiceImpl) GetDIDDocument(did string) (DidDocumentResponse, error) {
	resp := DidDocumentResponse{}

	// todo input validation

	identityAddr := ethcommon.HexToAddress(common.ConvertDIDToAddress(did))
	latestBlockNumber, err := s.contract.GetLatestRelatedBlock(nil, identityAddr)
	if err != nil {
		resp.ErrCode = constant.DID_DOES_NOT_EXIST
		return resp, nil
	}

	blockList := []uint64{}
	blockEventMap := map[uint64][]DIDAttributeChangedEventResponse{}
	// 1. resolve event history
	previousBlock := latestBlockNumber.Uint64()
	for previousBlock != STOP_RESOLVE_BLOCK_NUMBER {
		currentBlockNumber := previousBlock
		log.Printf("process block: %v", currentBlockNumber)
		blockList = append(blockList, currentBlockNumber)
		previousBlock = 0
		// 0206: seems that we can just use the iterator, maybe the loop enclosing this can be scrapped just set FilterOpts.Start to the STOP_RESOLVE_BLOCK_NUMBER

		// filter attribute changed event
		it, err := s.contract.FilterDIDAttributeChanged(&bind.FilterOpts{Start: currentBlockNumber, End: nil}, []ethcommon.Address{identityAddr})
		if err != nil {
			resp.ErrCode = constant.UNKNOW_ERROR
			return resp, nil
		}
		for it.Next() {
			// get the current log
			event := it.Event
			printDIDAttributeChangedEvent(event)
			if (len(event.Identity) == 0) || (event.Updated == nil) || (event.PreviousBlock == nil) {
				continue
			}
			identity := event.Identity.Hex()
			address := common.ConvertDIDToAddress(did)
			if identity != address {
				log.Printf("identity %v does not match did %v", identity, address)
				continue
			}

			// fill in block event map
			blockEventMap[currentBlockNumber] = append(blockEventMap[currentBlockNumber], SerializeDIDAttributeChangedEvent(event))
			previousBlock = event.PreviousBlock.Uint64()
			log.Printf("previous block set to: %v", previousBlock)
		}
		// panic("stop")
	}

	// 2. reverse block list to get the normal order
	for i, j := 0, len(blockList)-1; i < j; i, j = i+1, j-1 {
		blockList[i], blockList[j] = blockList[j], blockList[i]
	}

	doc := DidDocument{
		ID: did,
	}
	log.Printf("blockList: %v", blockList)
	log.Printf("blockEventMap: %v", blockEventMap)
	// 3. construct did document in normal order
	for _, blockNumber := range blockList {
		eventList := blockEventMap[blockNumber]
		for _, event := range eventList {
			constructDIDAttribute(string(event.Key), string(event.Value), did, &doc)
		}
	}

	resp.Doc = doc
	resp.ErrCode = constant.SUCCESS
	return resp, nil
}

func (s *DidServiceImpl) GetDIDDocumentJson(did string) (DidDocumentJsonResponse, error) {
	// TODO input validation
	resp := DidDocumentJsonResponse{}

	ret, err := s.GetDIDDocument(did)
	if err != nil {
		resp.ErrCode = ret.ErrCode
		return resp, err
	}
	doc := ret.Doc
	if len(doc.ID) == 0 {
		resp.ErrCode = ret.ErrCode
		return resp, errors.New("failed to get did document")
	}
	// encode the document into json
	data, err := doc.Encode()
	if err != nil {
		resp.ErrCode = ret.ErrCode
		return resp, nil
	}

	document := string(data)
	resp.Doc = fmt.Sprintf("%c%s%s", document[0], constant.DID_DOC_PROTOCOL_VERSION, document[1:])
	resp.ErrCode = ret.ErrCode
	return resp, nil
}

func (s *DidServiceImpl) setAttribute(didAddress string, attrKey string, attrVal string) (SetAttributeResponse, error) {
	resp := SetAttributeResponse{}
	// prepare contract auth
	auth, err := s.prepareContractAuth()
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	updated := big.NewInt(time.Now().UnixMilli())
	// covnert attrKey to 32 byte array
	attrKeyBytes := [32]byte{}
	copy(attrKeyBytes[:], []byte(attrKey))

	tx, err := s.contract.SetAttribute(auth, ethcommon.HexToAddress(didAddress), attrKeyBytes, []byte(attrVal), updated)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}
	// wait for the transaction to be mined
	receipt, err := s.WaitForTxnCommit(tx)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	// get the attribute changed event
	blockNumber := receipt.BlockNumber.Uint64()
	it, err := s.contract.FilterDIDAttributeChanged(&bind.FilterOpts{Start: blockNumber, End: nil}, []ethcommon.Address{ethcommon.HexToAddress(didAddress)})
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}

	ac := ReadDIDAttributeChangedEvent(it)
	if len(ac) == 0 {
		log.Fatal("DIDAttributeChangedEvent is empty")
		resp.ErrCode = constant.UNKNOW_ERROR
		return resp, nil
	}

	resp.Success = true
	resp.TxInfo.SetTxInfo(receipt)
	return resp, nil
}

func (s *DidServiceImpl) RevokePublicKeyWithAuth(did string, keyType string, owner string, ownerPublicKey string, privateKey string) (RevokePublicKeyWithAuthResponse, error) {
	// TODO input validation
	resp := RevokePublicKeyWithAuthResponse{}

	// get address from public key
	publicK, err := LoadPublicKey(ownerPublicKey)
	if err != nil {
		resp.ErrCode = constant.DID_PUBLICKEY_INVALID
		return resp, nil
	}
	address := crypto.PubkeyToAddress(*publicK)
	targetDid := common.ConvertAddressToDID(address.Hex())

	if strings.EqualFold(did, targetDid) {
		log.Printf("cannot remove the owning public key of this did: %v", did)
		resp.ErrCode = constant.DID_CANNOT_REMOVE_ITS_OWN_PUB_KEY_WITHOUT_BACKUP
		return resp, errors.New("cannot remove the owning public key of this did")
	}

	ret, err := s.GetDIDDocument(did)
	if err != nil || len(ret.Doc.ID) == 0 {
		resp.ErrCode = ret.ErrCode
		return resp, errors.New("failed to get did document")
	}

	isPublicKeyExit := false
	for _, pk := range ret.Doc.PublicKey {
		if strings.EqualFold(pk.PublicKey, ownerPublicKey) {
			if len(ret.Doc.PublicKey) == 1 {
				log.Printf("cannot remove the last public key of this did: %v", did)
				resp.ErrCode = constant.DID_CANNOT_REMOVE_ITS_OWN_PUB_KEY_WITHOUT_BACKUP
				return resp, errors.New("cannot remove the last public key of this did")
			}
			isPublicKeyExit = true
		}
	}

	if !isPublicKeyExit {
		log.Printf("public key %v does not exist in did %v", ownerPublicKey, did)
		resp.ErrCode = constant.DID_PUBLIC_KEY_NOT_EXIST
		return resp, errors.New("public key does not exist in did")
	}

	// add correct tag by externally call RevokeAuthentication once
	ret2, err := s.RevokeAuthentication(did, owner, ownerPublicKey, privateKey)
	if err != nil || !ret2.Success {
		log.Printf("failed to revoke authentication: %v", ret2.ErrCode)
		resp.Success = false
		resp.ErrCode = ret2.ErrCode
		return resp, errors.New("failed to revoke authentication")
	}

	didAddress := common.ConvertDIDToAddress(did)
	if len(owner) == 0 {
		owner = didAddress
	}

	attrKey := fmt.Sprintf("%s/%s/base64", constant.DID_DOC_PUBLICKEY_PREFIX, keyType)
	attrVal := fmt.Sprintf("%s%s|%s", ownerPublicKey, constant.REMOVED_PUBKEY_TAG, owner)

	r, err := s.setAttribute(didAddress, attrKey, attrVal)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}
	return RevokePublicKeyWithAuthResponse(r), nil
}

func (s *DidServiceImpl) RevokeAuthentication(did string, owner string, ownerPublicKey string, privateKey string) (RevokeAuthResponse, error) {
	// TODO input validation
	resp := RevokeAuthResponse{}

	ret, err := s.DidExist(did)
	if err != nil || !ret.Exist {
		resp.ErrCode = constant.DID_DOES_NOT_EXIST
		return resp, errors.New("did does not exist")
	}

	// get address
	didAddress := common.ConvertDIDToAddress(did)
	if owner == "" {
		owner = didAddress
	}

	attrKey := constant.DID_DOC_AUTHENTICATE_PREFIX
	attrVal := fmt.Sprintf("%s%s|%s", ownerPublicKey, constant.REMOVED_AUTHENTICATION_TAG, owner)

	r, err := s.setAttribute(didAddress, attrKey, attrVal)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}
	return RevokeAuthResponse(r), nil
}

// owner should be the address
func (s *DidServiceImpl) AddPublicKey(did string, keyType string, owner string, publicKey string, privateKey string) (AddPublicKeyResponse, error) {
	// TODO input validation
	resp := AddPublicKeyResponse{}

	didAddress := common.ConvertDIDToAddress(did)
	if len(owner) == 0 {
		owner = didAddress
	}

	ret, err := s.GetDIDDocument(did)
	if err != nil || len(ret.Doc.ID) == 0 {
		resp.ErrCode = ret.ErrCode
		return resp, errors.New("failed to get did document")
	}

	currentPubKeyId := len(ret.Doc.PublicKey)
	for _, pk := range ret.Doc.PublicKey {
		if strings.EqualFold(pk.PublicKey, publicKey) {
			if pk.Revoked {
				currentPubKeyId = int(pk.Id[len(pk.Id)-1])
			} else {
				log.Printf("public key %v already exists in did %v", publicKey, did)
				resp.ErrCode = constant.DID_PUBLIC_KEY_ALREADY_EXISTS
				return resp, errors.New("public key already exists in did")
			}
		}
	}

	// process set public key
	attrKey := fmt.Sprintf("%s/%s/base64", constant.DID_DOC_PUBLICKEY_PREFIX, keyType)
	attrVal := fmt.Sprintf("%s|%s", publicKey, owner)

	r, err := s.setAttribute(didAddress, attrKey, attrVal)
	if err != nil {
		resp.ErrCode = constant.TRANSACTION_EXECUTE_ERROR
		return resp, nil
	}
	resp.Val = currentPubKeyId
	resp.ServiceResponseInfo = r.ServiceResponseInfo
	return resp, nil
}

func (s *DidServiceImpl) GetDIDCount() (GetDidCountResponse, error) {
	resp := GetDidCountResponse{}
	total, err := s.contract.GetDIDCount(nil)
	if err != nil {
		resp.ErrCode = constant.UNKNOW_ERROR
		return resp, err
	} else {
		resp.Count = total.Uint64()
		resp.ErrCode = constant.SUCCESS
		return resp, nil
	}
}
