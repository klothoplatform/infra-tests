# @klotho::execution_unit {
#   id = "custom-dockerfile"
# }

FROM public.ecr.aws/lambda/nodejs:16

COPY package.json ./
RUN npm install
COPY . ./

ENV CUSTOM_DOCKERFILE=true

CMD [ "klotho_runtime/dispatcher.handler" ]
