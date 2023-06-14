package com.meca.did.controller;

import com.meca.did.constant.ErrorCode;
import com.meca.did.protocol.base.CptBaseInfo;
import com.meca.did.protocol.base.DIDAuthentication;
import com.meca.did.protocol.base.DIDPrivateKey;
import com.meca.did.protocol.request.CptMapArgs;
import com.meca.did.protocol.request.CptModel;
import com.meca.did.protocol.response.ResponseData;
import com.meca.did.service.CptService;
import com.meca.did.util.DataToolUtils;
import com.meca.did.util.PrivateKeyUtil;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@Api(tags = "CPT")
@AllArgsConstructor
@CrossOrigin
@RestController
@ConditionalOnProperty(prefix = "is", name = "issuer")
@RequestMapping("api/v1/cpt")
public class CptController {
    private static final Logger logger = LoggerFactory.getLogger(CptController.class);

    private final CptService cptService;

    /**
     * institutional publication of CPT.
     * claim is a JSON object
     *
     * @return returns CptBaseInfo
     */
    @ApiOperation(value = "Register CPT")
    @PostMapping("/register")
    public ResponseData<CptBaseInfo> registerCpt(
            @ApiParam(name = "cptModel", value = "CPT")
            @RequestBody CptModel cptModel) {

        ResponseData<CptBaseInfo> response;
        try {
            if (null == cptModel) {
                return new ResponseData<>(null, ErrorCode.ILLEGAL_INPUT);
            }
            String publisher = cptModel.getPublisher();
            String claim = DataToolUtils.mapToCompactJson(cptModel.getClaim());

            // get the private key from the file according to weId.
            String privateKey
                    = PrivateKeyUtil.getPrivateKeyByDID(PrivateKeyUtil.KEY_DIR, publisher);
            logger.info("param,publisher:{},privateKey:{},claim:{}", publisher, privateKey, claim);

            // converting claim in JSON format to map.
            Map<String, Object> claimMap = new HashMap<String, Object>();
            claimMap =
                    (Map<String, Object>) DataToolUtils.deserialize(
                            claim,
                            claimMap.getClass()
                    );

            DIDAuthentication dIDAuthentication = new DIDAuthentication();
            dIDAuthentication.setDID(publisher);
            dIDAuthentication.setDIDPrivateKey(new DIDPrivateKey());
            dIDAuthentication.getDIDPrivateKey().setPrivateKey(privateKey);

            CptMapArgs cptMapArgs = new CptMapArgs();
            cptMapArgs.setDIDAuthentication(dIDAuthentication);
            cptMapArgs.setCptJsonSchema(claimMap);

            // call method to register CPT on the chain.
            response = cptService.registerCpt(cptMapArgs);
            logger.info(
                    "registerCpt is result,errorCode:{},errorMessage:{}",
                    response.getErrorCode(),
                    response.getErrorMessage()
            );

            return response;
        } catch (Exception e) {
            logger.error("registerCpt error", e);
            return new ResponseData<>(null, ErrorCode.TRANSACTION_EXECUTE_ERROR);
        }
    }
}
